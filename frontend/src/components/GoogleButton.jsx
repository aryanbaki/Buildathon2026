import { useEffect } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

export default function GoogleButton() {
  const { login } = useAuth();

  useEffect(() => {
    function tryRender() {
      if (!CLIENT_ID) return;
      if (!window.google?.accounts?.id) {
        setTimeout(tryRender, 100);
        return;
      }
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: (response) => {
          const payload = JSON.parse(atob(response.credential.split(".")[1]));
          login({
            email:   payload.email,
            name:    payload.name,
            avatar:  payload.name?.[0]?.toUpperCase() || "G",
            picture: payload.picture,
            role:    "fleet_admin",
          });
        },
      });
      const btn = document.getElementById("g-btn");
      if (btn) {
        window.google.accounts.id.renderButton(btn, {
          theme: "outline", size: "large", width: 300, text: "signin_with_google",
        });
      }
    }
    setTimeout(tryRender, 300);
  }, []);

  if (!CLIENT_ID) return null;

  return <div id="g-btn" style={{ display: "flex", justifyContent: "center", minHeight: 44 }} />;
}
