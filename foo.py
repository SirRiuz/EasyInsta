import requests
import time
import uuid
import io
from PIL import Image

# ── Configuración ─────────────────────────────────────────────────────────────
BEARER    = "IGT:2:eyJkc191c2VyX2lkIjoiMzY2NzY3MTI2NTYiLCJzZXNzaW9uaWQiOiIzNjY3NjcxMjY1NiUzQUJvZGgzem5FQ0FoNTVwJTNBNyUzQUFZaHZtSGlSZVk5ckljdWIzZlpKaTV2b3o0WkpwRTdZM3JmMGw5Q1pGQSJ9"
WWW_CLAIM = "hmac.AR15DbrFJ725WBbDqzRf-QBsEkOsGLrMmREH-JEqRwW9yico"

DEVICE = {
    "user_agent": "Instagram 278.0.0.19.103 Android (31/12; 480dpi; 1440x3200; samsung; SM-S908B; b0s; exynos2200; en_US; 457547470)",
    "device_id":  "4EA5230C-6A2B-44E5-9542-E7A4149AC5BA",
    "android_id": "android-c2d5d1c487d24b4d",
    "pigeon_sid": "fa41a265-eca6-462d-b0fd-8da5bdc8f415",
}

# ── Headers base ──────────────────────────────────────────────────────────────
def base_headers() -> dict:
    return {
        "User-Agent":            DEVICE["user_agent"],
        "Authorization":         f"Bearer {BEARER}",
        "X-Ig-App-Id":           "936619743392459",
        "X-Ig-Capabilities":     "3brTPw==",
        "X-Ig-Connection-Type":  "WIFI",
        "X-Ig-Device-Id":        DEVICE["device_id"],
        "X-Ig-Android-Id":       DEVICE["android_id"],
        "X-Ig-Timezone-Offset":  "-18000",
        "X-Ig-Www-Claim":        WWW_CLAIM,
        "X-Ig-App-Locale":       "en_US",
        "X-Ig-Device-Locale":    "en_US",
        "X-Ig-Mapped-Locale":    "en_US",
        "X-Pigeon-Session-Id":   DEVICE["pigeon_sid"],
        "X-Pigeon-Rawclienttime": f"{time.time():.3f}",
        "Accept-Language":       "en-US",
        "Accept-Encoding":       "gzip, deflate",
    }

# ── Paso 0 — Descargar imagen desde URL ───────────────────────────────────────
def download_image(url: str) -> bytes:
    print(f"📥 Descargando imagen desde: {url}")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    # Convertir a JPEG con Pillow para asegurar formato correcto
    img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    data = buf.getvalue()
    print(f"   Tamaño: {len(data) / 1024:.1f} KB")
    return data

# ── Paso 1 — Upload de la imagen ──────────────────────────────────────────────
def upload_photo(image_data: bytes) -> str | None:
    upload_id   = str(int(time.time() * 1000))
    entity_name = f"{upload_id}_0_{uuid.uuid4().int & 0xFFFFFFFF}"
    content_len = len(image_data)

    print(f"\n📤 Subiendo imagen...")
    print(f"   upload_id   : {upload_id}")
    print(f"   entity_name : {entity_name}")

    headers = base_headers()
    headers.update({
        "X-Instagram-Rupload-Params": f'{{"upload_id":"{upload_id}","media_type":"1"}}',
        "X-Entity-Type":   "image/jpeg",
        "X-Entity-Name":   entity_name,
        "X-Entity-Length": str(content_len),
        "Offset":          "0",
        "Content-Type":    "application/octet-stream",
        "Content-Length":  str(content_len),
    })

    resp = requests.post(
        f"https://i.instagram.com/rupload_igphoto/{entity_name}/",
        headers=headers,
        data=image_data,
    )

    print(f"   Status  : {resp.status_code}")
    print(f"   Response: {resp.text}")

    if resp.status_code == 200 and resp.json().get("status") == "ok":
        print(f"   ✅ Upload exitoso")
        return upload_id

    print(f"   ❌ Upload falló")
    return None

# ── Paso 2 — Cambiar foto de perfil ──────────────────────────────────────────
def change_profile_picture(upload_id: str) -> bool:
    print(f"\n🔄 Actualizando foto de perfil...")

    headers = base_headers()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    payload = {
        "upload_id":             upload_id,
        "use_fbuploader":        "true",
        "remove_birthday_selfie": "False",
        "_uuid":                 DEVICE["device_id"],
    }

    resp = requests.post(
        "https://i.instagram.com/api/v1/accounts/change_profile_picture/",
        headers=headers,
        data=payload,
    )

    print(f"   Status  : {resp.status_code}")
    print(f"   Response: {resp.text}")

    if resp.status_code == 200:
        print("   ✅ Foto de perfil actualizada")
        return True

    print("   ❌ Error al actualizar foto")
    return False

# ── Main ──────────────────────────────────────────────────────────────────────
def update_profile_picture(image_url: str):
    print("=" * 50)
    print("Instagram — Cambiar foto de perfil")
    print("=" * 50)

    # Paso 0 — Descargar
    image_data = download_image(image_url)

    # Paso 1 — Upload
    upload_id = upload_photo(image_data)
    if not upload_id:
        print("\n❌ Proceso cancelado — upload falló")
        return

    # Paso 2 — Actualizar perfil
    change_profile_picture(upload_id)

if __name__ == "__main__":
    IMAGE_URL = "https://instagram.fbga1-3.fna.fbcdn.net/v/t51.82787-15/656805425_18722149726056421_7229925617792459234_n.jpg?stp=dst-jpg_e35_p1080x1080_tt6&_nc_cat=1&ig_cache_key=Mzg3MDI1NDIxMDk3Mjk1MTU2NQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6InhwaWRzLjE0NDB4MTc5OS5zZHIuQzMifQ%3D%3D&_nc_ohc=cwLQfrnflD4Q7kNvwEWR4Ok&_nc_oc=AdqogZReoh-7mzY0ZZyDe5LcBHmNSsRHW1J1MxY8vRs3FehPGCpYFh_3Hga5vdon1UU&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=instagram.fbga1-3.fna&_nc_gid=wiOxeXiCt5mfmSAwC2MMmQ&_nc_ss=7a32e&oh=00_Af0VU58roKCtuyLIQHOx2_HeJTbS2aYUnfxhWD2ZD5xPGw&oe=69E355EA"
    update_profile_picture(IMAGE_URL)