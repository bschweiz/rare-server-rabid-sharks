import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from postTags import *
from posts import *
from tags import *
from comments import *
from users import *
from categories import *




class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed
            

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            elif resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == "post_tags":
                    response = f"{get_all_Post_tags()}"
            # 5elif resource == "locations":
            #     if id is not None:
            #         response = f"{get_single_location(id)}"
            #     else:
            #         response = f"{get_all_locations()}"
            elif resource == "comments":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "users":
                response = get_user_by_email(value)

            elif key == "post_id" and resource == "post_tags":
                response = get_post_tags_by_post_id(value)

            elif key == "user_id" and resource == "posts":
                response = get_posts_by_user_id(value)

            if key == "post_id" and resource == "comments":
                response = get_comments_by_post_id(value)

        self.wfile.write(response.encode())

        # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        print(resource)
        # Initialize new animal
        new_entry = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "posts":
            new_entry = create_post(post_body)
        elif resource == "tags":
            new_entry = create_tag(post_body)
        elif resource == "users":
            new_entry = create_user(post_body)
        elif resource == "categories":
            new_entry = create_category(post_body)
        elif resource == "post_tags":
            new_entry = accept_tag_array_by_post_id(post_body)
        elif resource == "comments":
            new_entry = create_comment(post_body)
        elif resource == "login":
            new_entry = login_user(post_body)
        elif resource == "register":
            new_entry = create_user(post_body)
        # Encode the new animal and send in response
        self.wfile.write(f"{new_entry}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "posts":
            delete_post(id)
        elif resource == "tags":
            delete_tag(id)
        elif resource == "categories":
            delete_category(id)
        elif resource == "post_tags":
            delete_post_tag(id)
        elif resource == "comments":
            delete_comment(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())
        # Here's a method on the class that overrides the parent's method.
        # It handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "posts":
            update_post(id, post_body)
        elif resource == "tags":
            update_tag(id, post_body)
        elif resource == "post_tags":
            update_post_tag(id, post_body)
        # elif resource == "locations":
        #     update_location(id, post_body)
        elif resource == "comments":
            update_comment(id, post_body)
        elif resource == "users":
            update_user(id, post_body)
        elif resource == "categories":
            update_category(id, post_body)
        # elif resource == "locations":
        #     update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()