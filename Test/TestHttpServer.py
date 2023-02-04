# Main server functions to be handled by clients

import http.server
import json
import os.path


# Crude Http Server to reply to incoming requests
class RESTFullServer(http.BaseHTTPRequestHandler):
    stacks = json.dumps({[]})
    current_id = 0
    current_op = 'none'

    def do_GET(self):
        if self.path == '/rpn/op':
            self.do_get_op(self)
        elif self.path == '/rpn/stack':
            self.do_get_stacks(self)
        elif '/rpn/stack/' in self.path:
            self.current_id = os.path.basename(self.path)
            self.do_get_stack(self, self.current_id)

    def do_POST(self):
        if self.path == '/rpn/stack':
            self.do_post_new_stack(self)
        elif '/rpn/stack/' in self.path:
            self.current_id = os.path.basename(self.path)
            self.do_post_stack_value(self, self.current_id)
        elif '/rpn/op/' in self.path:
            head_tail = os.path.split(self.path)
            stack_id = head_tail[1]
            head_tail2 = os.path.split(head_tail)
            head_tail3 = os.path.split(head_tail2[0])
            op_id = head_tail3[1]
            self.do_apply_operand(self, stack_id, op_id)

    def do_DELETE(self):
        if '/rpn/stack/' in self.path:
            self.current_id = os.path.basename(self.path)
            self.do_delete_stack(self, self.current_id)

    # GET OPERATIONS
    def do_get_op(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({'operands': ['add_element', 'recover_stack', 'clean_stack', 'plus_op', 'minus_op',
                                                  'factor_op', 'divide_op', 'none']}))

    def do_get_stacks(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.stacks))

    def do_get_stack(self, stack_id):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.stacks[stack_id]))

    # POST OPERATIONS
    def do_post_new_stack(self):
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        stack_count = self.stacks.count()
        self.stacks.insert({"id": stack_count + 1, "stack": []})
        self.wfile.write(json.dumps({'stack_id': stack_count + 1, 'status': "added"}))

    def do_post_stack_value(self, stack_id):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        self.stacks[stack_id]["stack"].append(message['value'])
        self.wfile.write(json.dumps({'stack_id': stack_id, 'value_added': message['value']}))

    def do_apply_operand(self, stack_id, op_id):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        stack_content = self.stacks[stack_id]['stack']
        i = 0
        values = []
        for content in stack_content:
            i += 1
            values.append(content)
        if op_id == 'plus_op':
            new_val = int(values[i]) + int(values[i - 1])
        elif op_id == 'minus_op':
            new_val = int(values[i]) - int(values[i - 1])
        elif op_id == 'factor_op':
            new_val = int(values[i]) * int(values[i - 1])
        elif op_id == 'divide_op':
            new_val = int(values[i]) / int(values[i - 1])

        self.stacks[stack_id]['stack'].pop(i)
        self.stacks[stack_id]['stack'].pop(i-1)
        self.stacks[stack_id]['stack'].append(new_val)

        self.wfile.write(json.dumps({'stack_id': stack_id, 'operand': op_id}))

    # DELETE OPERATIONS
    def do_delete_stack(self, stack_id):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.stacks.pop(stack_id)
        self.wfile.write(json.dumps({'stack_id': stack_id, 'status': "deleted"}))
