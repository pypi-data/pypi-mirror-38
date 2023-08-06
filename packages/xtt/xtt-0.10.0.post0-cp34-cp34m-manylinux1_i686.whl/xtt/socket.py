# Copyright 2018 Xaptum, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

from __future__ import absolute_import
from __future__ import print_function

import socket

from xtt import Identity
from xtt.certificates import ECDSAP256RootCertificateContext, CertificateRootId
from xtt.server import ServerCookieContext, ServerHandshakeContext
from xtt.client import ClientHandshakeContext

from xtt.exceptions import *

__all__ = ['XTTClientSocket', 'XTTServerSocket']

class XTTClientSocket(object):

    def __init__(self, sock, version, suite_spec, group_context, server_id,
                 root_id, root_pubkey, identity=None):
        self._sock = sock
        self._server_root_id = CertificateRootId()
        self._root_cert = ECDSAP256RootCertificateContext(root_id, root_pubkey)
        self._server_id = server_id
        self._identity  = identity or Identity()
        self._group_ctx = group_context
        self._ctx = ClientHandshakeContext(version, suite_spec)

    @property
    def identity(self):
        return self._ctx.my_identity

    @property
    def longterm_public_key(self):
        return self._ctx.my_longterm_public_key_ecdsap256

    @property
    def longterm_private_key(self):
        return self._ctx.my_longterm_private_key_ecdsap256

    def _do(self, step, *args):
        try:
            step(*args)
        except XTTWantReadError:
            self.do_read()
        except XTTWantWriteError:
            self.do_write()
        except XTTWantPreparseServerAttestError:
            self.do_preparse_server_attest()
        except XTTWantBuildIdClientAttestError:
            self.do_build_id_client_attest()
        except XTTWantParseIdServerFinishedError:
            self.do_parse_id_server_finished()

    def start(self):
        self._do(self._ctx.start)

    def do_read(self):
        buf = self._ctx.io_buffer
        cnt = self._sock.recv_into(buf, len(buf))
        if cnt == 0:
            raise socket.error("EOF")
        self._do(self._ctx.handle_io, 0, cnt)

    def do_write(self):
        buf = self._ctx.io_buffer
        cnt = self._sock.send(buf)
        self._do(self._ctx.handle_io, cnt, 0)

    def do_preparse_server_attest(self):
        self._do(self._ctx.preparse_server_attest, self._server_root_id)

    def do_build_id_client_attest(self):
        self._do(self._ctx.build_id_client_attest,
                 self._root_cert,
                 self._server_id,
                 self._identity,
                 self._group_ctx)

    def do_parse_id_server_finished(self):
        self._do(self._ctx.parse_id_server_finished)

class XTTServerSocket(object):

    def __init__(self, sock, cert_context, group_from_id, assign_client_id):
        self._sock = sock
        self._cert_ctx = cert_context
        self._cookie_ctx = ServerCookieContext()
        self._group_from_id = group_from_id
        self._assign_client_id = assign_client_id
        self._ctx = ServerHandshakeContext()

    def _do(self, step, *args):
        try:
            step(*args)
        except XTTWantReadError:
            self.do_read()
        except XTTWantWriteError:
            self.do_write()
        except XTTWantBuildServerAttestError:
            self.do_build_server_attest()
        except XTTWantPreparseIdClientAttestError:
            self.do_preparse_id_client_attest()
        except XTTWantVerifyGroupSignatureError:
            self.do_verify_group_signature()
        except XTTWantBuildIdServerFinishedError:
            self.do_build_id_server_finished()

    def handle_connect(self):
        self._do(self._ctx.handle_connect)

    def do_read(self):
        buf = self._ctx.io_buffer
        cnt = self._sock.recv_into(buf, len(buf))
        if cnt == 0:
            raise socket.error("EOF")
        self._do(self._ctx.handle_io, 0, cnt)

    def do_write(self):
        buf = self._ctx.io_buffer
        cnt = self._sock.send(buf)
        self._do(self._ctx.handle_io, cnt, 0)

    def do_build_server_attest(self):
        self._do(self._ctx.build_server_attest, self._cert_ctx, self._cookie_ctx)

    def do_preparse_id_client_attest(self):
        self._do(self._ctx.preparse_id_client_attest, self._cert_ctx, self._cookie_ctx)

    def do_verify_group_signature(self):
        group = self._group_from_id(self._ctx.client_claimed_group)
        if not group:
            raise ValueError("Invalid Group")
        self._do(self._ctx.verify_group_signature, group, self._cert_ctx)

    def do_build_id_server_finished(self):
        assigned_id = self._assign_client_id(self._ctx.client_requested_identity,
                                             self._ctx.client_claimed_group,
                                             self._ctx.client_pseudonym_lrsw)
        if not assigned_id:
            raise ValueError("Invalid Identity")
        self._do(self._ctx.build_id_server_finished, assigned_id)
