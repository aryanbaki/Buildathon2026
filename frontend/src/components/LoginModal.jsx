import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const VALID_CODE = "248613";

function GoogleButton({ onLogin }) {
  useEffect(() => {
    function tryRender() {
      if (!window.google?.accounts?.id) { setTimeout(tryRender, 150); return; }
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: (res) => {
          const p = JSON.parse(atob(res.credential.split(".")[1]));
          onLogin({ email: p.email, name: p.name, avatar: p.name?.[0]?.toUpperCase() || "G", role: "fleet_admin" });
        },
      });
      const el = document.getElementById("g-signin-btn");
      if (el) window.google.accounts.id.renderButton(el, { theme: "outline", size: "large", width: 300 });
    }
    setTimeout(tryRender, 300);
  }, []);
  return <div id="g-signin-btn" style={{ display:"flex", justifyContent:"center", minHeight:44 }} />;
}

const delay = ms => new Promise(r => setTimeout(r, ms));

export default function LoginModal() {
  const { login, setShowLogin } = useAuth();
  const [step, setStep]       = useState("email");
  const [email, setEmail]     = useState("");
  const [password, setPass]   = useState("");
  const [code, setCode]       = useState("");
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);

  async function handleEmail(e) {
    e.preventDefault(); setError("");
    if (!email.includes("@")) { setError("Enter a valid email."); return; }
    setLoading(true); await delay(700); setLoading(false); setStep("password");
  }
  async function handlePassword(e) {
    e.preventDefault(); setError("");
    if (password.length < 6) { setError("Password must be at least 6 characters."); return; }
    setLoading(true); await delay(900); setLoading(false); setStep("twofa");
  }
  async function handleTwoFA(e) {
    e.preventDefault(); setError("");
    setLoading(true); await delay(600); setLoading(false);
    if (code !== VALID_CODE) { setError("Wrong code. Demo: 248613"); return; }
    login({ email, name: email.split("@")[0], avatar: email[0].toUpperCase(), role: "fleet_admin" });
  }

  return (
    <div style={{ position:"fixed",inset:0,background:"rgba(0,0,0,.55)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:1000,padding:20 }}>
      <div style={{ background:"#fff",borderRadius:16,width:"100%",maxWidth:400,boxShadow:"0 24px 60px rgba(0,0,0,.2)",overflow:"hidden",position:"relative" }}>

        {/* X close button */}
        <button
          onClick={() => setShowLogin(false)}
          style={{ position:"absolute",top:12,left:14,background:"none",border:"none",color:"#9898B0",fontSize:22,cursor:"pointer",zIndex:10,lineHeight:1 }}
        >✕</button>

        <div style={{ background:"#1A1A2E",padding:"28px 32px 24px",textAlign:"center" }}>
          <div style={{ fontSize:28,marginBottom:8 }}>🚛</div>
          <div style={{ color:"#fff",fontSize:18,fontWeight:600 }}>Fleet Document Intelligence</div>
          <div style={{ color:"#9898B0",fontSize:13,marginTop:4 }}>Sign in to your account</div>
        </div>

        <div style={{ padding:"28px 32px" }}>
          <div style={{ display:"flex",gap:6,marginBottom:24 }}>
            {["email","password","twofa"].map((s,i) => (
              <div key={s} style={{ flex:1,height:3,borderRadius:99,background:["email","password","twofa"].indexOf(step)>=i?"#F4A622":"#E4E2D9",transition:"background .3s" }} />
            ))}
          </div>

          {step === "email" && (
            <form onSubmit={handleEmail}>
              <div style={{ marginBottom:16 }}>
                <label style={L}>Email address</label>
                <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@company.com" autoFocus style={I} />
              </div>
              {error && <div style={ER}>{error}</div>}
              <button type="submit" disabled={loading} style={BP}>{loading?"Checking…":"Continue →"}</button>
              <div style={{ display:"flex",alignItems:"center",gap:10,margin:"20px 0" }}>
                <div style={{ flex:1,height:1,background:"#E4E2D9" }} />
                <span style={{ fontSize:12,color:"#9C9890" }}>or</span>
                <div style={{ flex:1,height:1,background:"#E4E2D9" }} />
              </div>
              {CLIENT_ID
                ? <GoogleButton onLogin={login} />
                : <button type="button" onClick={()=>login({email:"demo@fleetai.com",name:"Demo User",avatar:"D",role:"fleet_admin"})} style={BG}>Sign in with Google (demo)</button>
              }
            </form>
          )}

          {step === "password" && (
            <form onSubmit={handlePassword}>
              <div style={{ fontSize:13,color:"#6B6965",marginBottom:4 }}>Signing in as <strong>{email}</strong></div>
              <button type="button" onClick={()=>setStep("email")} style={BB}>← Change email</button>
              <div style={{ marginBottom:16,marginTop:16 }}>
                <label style={L}>Password</label>
                <input type="password" value={password} onChange={e=>setPass(e.target.value)} placeholder="Enter your password" autoFocus style={I} />
              </div>
              {error && <div style={ER}>{error}</div>}
              <button type="submit" disabled={loading} style={BP}>{loading?"Verifying…":"Sign in →"}</button>
            </form>
          )}

          {step === "twofa" && (
            <form onSubmit={handleTwoFA}>
              <div style={{ textAlign:"center",marginBottom:20 }}>
                <div style={{ fontSize:32,marginBottom:8 }}>🔐</div>
                <div style={{ fontSize:15,fontWeight:600,marginBottom:4 }}>Two-step verification</div>
                <div style={{ fontSize:13,color:"#6B6965" }}>Enter the 6-digit code from your authenticator app.</div>
              </div>
              <div style={{ marginBottom:16 }}>
                <label style={L}>Verification code</label>
                <input type="text" value={code} onChange={e=>setCode(e.target.value.replace(/\D/g,"").slice(0,6))} placeholder="000000" autoFocus maxLength={6}
                  style={{ ...I,fontSize:24,textAlign:"center",letterSpacing:8,fontWeight:600 }} />
                <div style={{ fontSize:11,color:"#9C9890",marginTop:6,textAlign:"center" }}>Demo code: <strong>248613</strong></div>
              </div>
              {error && <div style={ER}>{error}</div>}
              <button type="submit" disabled={loading||code.length<6} style={BP}>{loading?"Verifying…":"Verify & Sign in"}</button>
              <button type="button" onClick={()=>setStep("password")} style={{ ...BB,marginTop:12 }}>← Back</button>
            </form>
          )}
        </div>

        <div style={{ padding:"0 32px 20px",textAlign:"center",fontSize:11,color:"#9C9890" }}>
          AI Buildathon Dallas 2026 · Secure fleet document access
        </div>
      </div>
    </div>
  );
}

const L  = { display:"block",fontSize:12,fontWeight:600,color:"#6B6965",marginBottom:6,textTransform:"uppercase",letterSpacing:".05em" };
const I  = { width:"100%",padding:"10px 14px",fontSize:15,border:"1px solid #E4E2D9",borderRadius:8,outline:"none",background:"#FAFAFA" };
const ER = { fontSize:12,color:"#DC2626",background:"#FEE2E2",border:"1px solid #FECACA",borderRadius:8,padding:"8px 12px",marginBottom:12 };
const BP = { width:"100%",padding:"11px",background:"#F4A622",color:"#fff",border:"none",borderRadius:8,fontSize:14,fontWeight:600,cursor:"pointer" };
const BG = { width:"100%",padding:"10px",background:"#fff",color:"#1C1C1E",border:"1px solid #E4E2D9",borderRadius:8,fontSize:14,cursor:"pointer" };
const BB = { background:"none",border:"none",fontSize:12,color:"#9C9890",cursor:"pointer",padding:0 };
