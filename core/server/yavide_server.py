import sys
import argparse
import logging
from common.yavide_utils import YavideUtils
from syntax.syntax_highlighter.syntax_highlighter import VimSyntaxHighlighter
from syntax.syntax_highlighter.tag_identifier import TagIdentifier
from multiprocessing import Process, Queue

# TODO remove. Used only for sleep() 
import time

class Client():
    def __init__(self, server_queue, server_name):
        self.queue = Queue()
        self.server_queue = server_queue
        self.server_name = server_name

    def startup_impl(self, data):
        return

    def shutdown_impl(self, data):
        return

    def run_impl(self, data):
        return

    def run(self):
        while True:
            data = self.queue.get()
            if data[0] == 'STARTUP':
                self.startup_impl(data[1])
            elif data[0] == 'SHUTDOWN':
                self.shutdown_impl(data[1])
                break
            else:
                self.run_impl(data[1])

class SourceCodeHighlighter(Client):
    def __init__(self, server_queue, server_name):
        Client.__init__(self, server_queue, server_name)
        self.output_directory = "/tmp"
        self.tag_id_list = [
            TagIdentifier.getClassId(),
            TagIdentifier.getClassStructUnionMemberId(),
            TagIdentifier.getEnumId(),
            TagIdentifier.getEnumValueId(),
            TagIdentifier.getExternFwdDeclarationId(),
            TagIdentifier.getFunctionDefinitionId(),
            TagIdentifier.getFunctionPrototypeId(),
            TagIdentifier.getLocalVariableId(),
            TagIdentifier.getMacroId(),
            TagIdentifier.getNamespaceId(),
            TagIdentifier.getStructId(),
            TagIdentifier.getTypedefId(),
            TagIdentifier.getUnionId(),
            TagIdentifier.getVariableDefinitionId()
        ]
        self.syntax_highlighter = VimSyntaxHighlighter(self.tag_id_list, self.output_directory)

    def run_impl(self, filename):
        self.syntax_highlighter.generate_vim_syntax_file(filename)
        YavideUtils.send_vim_remote_command(self.server_name, ":call Y_CodeHighlight_Apply('" + filename + "')")

def yavide_server_run(server_queue, server_name):
    YavideUtils.send_vim_remote_command(server_name, ":echomsg '" + server_name + "'")
    clients = [SourceCodeHighlighter(server_queue, server_name)]
    client_processes = []
    for client in clients:
        p = Process(target=client.run)
        p.daemon = False
        p.start()
        client_processes.append(p)

    while True:
        YavideUtils.send_vim_remote_command(server_name, ":echomsg 'Waiting for a message ...'")
        data = server_queue.get()
        YavideUtils.send_vim_remote_command(server_name, ":echomsg 'message recvd'")
        if data[2] == 'SHUTDOWN':
            YavideUtils.send_vim_remote_command(server_name, ":echomsg 'SHUTDOWN recvd'")
            for client in clients:
                client.queue.put(['SHUTDOWN', 0])
            break
            YavideUtils.send_vim_remote_command(server_name, ":echomsg 'SHUTDOWN sent'")
        else:
            YavideUtils.send_vim_remote_command(server_name, ":echomsg 'payload" + data[2] + "'")
            client.queue.put(['REQUEST', data[2]])

    YavideUtils.send_vim_remote_command(server_name, ":echomsg 'joining clients ...'")
    for process in client_processes:
        process.join()

