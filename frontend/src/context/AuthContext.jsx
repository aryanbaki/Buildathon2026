import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("fleet_user")); } catch { return null; }
  });
  const [showLogin, setShowLogin] = useState(false);

  useEffect(() => {
    if (!user) setShowLogin(true);
  }, []);

  function login(userData) {
    localStorage.setItem("fleet_user", JSON.stringify(userData));
    setUser(userData);
    setShowLogin(false);
  }

  function logout() {
    localStorage.removeItem("fleet_user");
    setUser(null);
    setShowLogin(true);
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, showLogin, setShowLogin }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() { return useContext(AuthContext); }
