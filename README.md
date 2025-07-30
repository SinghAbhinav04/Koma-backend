# **Koma Backend**  
The backend powering **Koma-AI**, an AI-driven platform for **manga generation** using **Google Gemini**.  
Built with **Flask**, **MongoDB**, and **Cloudinary**, this backend handles **secure user authentication**, **encrypted API key storage**, and **manga generation logic**.

**Live Application:** [https://www.koma-ai.app](https://www.koma-ai.app)  
**Hosted on:** [Railway](https://railway.app)

---

## **Core Features**  
### **AI Manga Generation Pipeline**  
- Refines user prompts via **Gemini text model**.  
- Breaks story into **6 subplots** → Generates each manga panel with **Gemini image model**.  
- Combines panels into a grid using **PIL**.  
- Uploads final image to **Cloudinary** and stores the URL in MongoDB.  

### **User Authentication**  
- Registration & login with **hashed passwords** using `crypt` (with salt).  

### **API Key Security**  
- Gemini API key is **encrypted with AES cipher** using `crypto` before storing in MongoDB.  
- Decrypted **only in backend memory for API calls**.  
- **Never exposed to the client or logs**.  

### **User Features**  
- View personal manga gallery.  
- Like comics & manage history.  

---

## **Security Practices**  
- **Passwords:** Hashed with `crypt` and salted.  
- **API Keys:**  
  - Encrypted using AES before DB storage.  
  - Decrypted in-memory during Gemini calls.  
  - Never sent to client or stored in plaintext.  
- **All data transfers over HTTPS (Railway hosting)**.  

---

## **Manga Generation Workflow**
1. User submits a **prompt** via frontend.  
2. Backend uses Gemini to **refine prompt** and create **6 unique subplots**.  
3. Gemini image API generates **6 panels**.  
4. Panels are merged into a manga grid with **PIL**.  
5. Composite image uploaded to **Cloudinary** → URL stored in MongoDB.  

---

## **Project Structure**

## **Project Structure**
```plaintext
koma-backend/
├── app.py                   # Flask entry point
├── requirements.txt         # Dependencies
├── models/
│   └── user_schema.py       # MongoDB schema for users
├── routes/
│   ├── auth.py              # User authentication
│   └── manga.py             # Manga generation & gallery
├── utils/
│   ├── cloudinary_upload.py # Handles image upload to Cloudinary
│   ├── encrypt_decrypt.py   # AES encryption & decryption for API keys
│   ├── jwt_handler.py       # JWT token generation & validation
│   └── manga_gen.py         # Gemini prompt refinement & panel generation logic

```

---

## **Tech Stack**
- **Framework:** Flask  
- **Database:** MongoDB  
- **Media Storage:** Cloudinary  
- **AI Integration:** Google Gemini (Text + Image)  
- **Security:** AES encryption for keys, salted password hashing, JWT auth  

---

## **Deployment**
- Hosted on **Railway**  
- Environment variables managed securely  
- HTTPS enabled  

---

## **License**
Custom License – **Personal & Educational Use Only (No Commercial Use Without Permission)**  
[View License](./LICENSE)
