import uvicorn

if __name__ == '__main__':
    uvicorn.run("api.app:app" , reload=True, host='localhost', port=5000)
