from wsgiref.simple_server import make_server
import falcon
import resources


cors = falcon.CORSMiddleware(allow_origins="*", allow_credentials="*")
app = falcon.App(middleware=cors)

app.add_route("/", resources.RedirectResource())
app.add_route("/estimate", resources.EstimationResource())
app.add_route("/success", resources.SuccessCallbackResource())
app.add_route("/failure", resources.FailureCallbackResource())

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
