from wsgiref.simple_server import make_server
import falcon
import resources




app = falcon.App(
    middleware=falcon.CORSMiddleware(allow_origins="*", allow_credentials="*")
)
app.add_route("/success", resources.SuccessCallbackResource())
app.add_route("/failure", resources.FailureCallbackResource())
app.add_route("/estimate", resources.EstimationResource())
app.add_route("/", resources.RedirectResource())

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
