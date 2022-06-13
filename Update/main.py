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

# model
class Mahasiswa(BaseModel):
  npm: str
  nama: str

# utility error
def invalid_param_error():
  response = {
    "status": "ERROR",
    "message": "parameter tidak valid"
  }
  return response

# endpoint
@app.post("")
async def update_mahasiswa(mahasiswa: Mahasiswa):
  try:
    query = f"""
      INSERT INTO mahasiswa VALUES ('{mahasiswa.npm}', '{mahasiswa.nama}')
      ON CONFLICT (npm) DO UPDATE
        SET nama='{mahasiswa.nama}'
      RETURNING *;
    """

    DB_CURSOR.execute(query)
    DB_CONN.commit()
    response = { "status": "OK" }
  except:
    DB_CURSOR.execute("ROLLBACK")
    response = invalid_param_error()
  return response


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=int(config('APP_PORT')))