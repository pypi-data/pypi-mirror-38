def get_auth_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJuYW1lIjoiU2lkZGhhbnQgVWpqYWluIiwiZW1haWwiOiJzaWRkaGFudC51amphaW5AZ21haWwuY29tIiwiaWF0IjoxNTM4OTkxNzI4LCJleHAiOjE1MzkwMjc3Mjh9.cRKmgtvqhMinOdDYVn5VWwSIZl_7wxFWayYF73rw15Y"


def get_auth_header():
    return {"Authorization": f"Bearer {get_auth_token()}"}
