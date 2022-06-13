from decouple import config
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import uvicorn

# init
app = FastAPI()

DB_CONN = psycopg2.connect(
    host=config('DB_HOST'),
    database=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASS')
)

DB_CURSOR = DB_CONN.cursor()

# utility error
def mahasiswa_not_found_error():
  response = {
    "status": "ERROR",
    "message": "mahasiswa tidak ditemukan"
  }
  return response

# endpoint
@app.get("/read/{npm}")
async def read_user(npm: str):
  try:
    query = f"""
      SELECT * FROM mahasiswa
      WHERE npm='{npm}';
    """

    DB_CURSOR.execute(query)

    data = DB_CURSOR.fetchone()
    response = {
      "status": "OK",
      "npm": data[0],
      "nama": data[1]
    }
  except:
    response = mahasiswa_not_found_error()
  return response


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=int(config('APP_PORT')))