// Authentication Helper Functions
const API_BASE_URL = "http://localhost:5000/api";

// Token Management
const TokenManager = {
  set: (token) => localStorage.setItem("authToken", token),
  get: () => localStorage.getItem("authToken"),
  remove: () => localStorage.removeItem("authToken"),
  exists: () => !!localStorage.getItem("authToken"),
};

// User Management
const UserManager = {
  set: (user) => localStorage.setItem("user", JSON.stringify(user)),
  get: () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  },
  remove: () => localStorage.removeItem("user"),
  isLoggedIn: () => TokenManager.exists() && !!UserManager.get(),
};

// API Helper
async function apiRequest(endpoint, method = "GET", data = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  const token = TokenManager.get();
  if (token) {
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  if (data && (method === "POST" || method === "PUT" || method === "PATCH")) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Request failed");
    }

    return result;
  } catch (error) {
    throw error;
  }
}

// Check Authentication Status
async function checkAuthStatus() {
  // If token doesn't exist, user is not authenticated
  if (!TokenManager.exists()) {
    return false;
  }

  // If user data exists in localStorage, assume authenticated
  // This avoids unnecessary API calls on every page load
  if (UserManager.get()) {
    return true;
  }

  // Only verify with API if user data is missing
  try {
    const result = await apiRequest("/verify-token", "GET");
    if (result.valid) {
      return true;
    } else {
      // Token is invalid
      TokenManager.remove();
      UserManager.remove();
      return false;
    }
  } catch (error) {
    // Token is invalid or network error
    TokenManager.remove();
    UserManager.remove();
    return false;
  }
}

// Protected Pages List
const PROTECTED_PAGES = [
  "our-work.html",
  "pricing.html",
  "our-team.html",
  "about.html",
  "contact.html",
];

// Check if current page requires authentication
function isProtectedPage() {
  const currentPage = window.location.pathname.split("/").pop();
  return PROTECTED_PAGES.includes(currentPage);
}

// IMMEDIATE PROTECTION - Hide page before it renders if protected and not logged in
(function () {
  if (isProtectedPage()) {
    // Check if user has token AND user data (both required for authentication)
    const hasToken = TokenManager.exists();
    const hasUserData = !!UserManager.get();

    if (!hasToken || !hasUserData) {
      // Immediately hide page and redirect
      document.documentElement.style.visibility = "hidden";
      const returnUrl = encodeURIComponent(window.location.pathname);
      window.location.replace(`/login.html?return=${returnUrl}`);
    }
  }
})();

// Redirect to login with return URL
function redirectToLogin() {
  const returnUrl = encodeURIComponent(window.location.pathname);
  window.location.href = `/login.html?return=${returnUrl}`;
}

// Initialize page protection (simplified - main check is done above)
async function initPageProtection() {
  // The immediate IIFE above handles protection
  // This function is kept for compatibility but does nothing now
  // since we rely on synchronous localStorage checks
}

// Update Navigation Based on Auth Status
function updateNavigation() {
  const navButtons = document.querySelector(".nav-buttons");
  if (!navButtons) return;

  const isLoggedIn = UserManager.isLoggedIn();

  if (isLoggedIn) {
    const user = UserManager.get();
    navButtons.innerHTML = `
            <span class="user-greeting" style="color: var(--text-dark); margin-right: 1rem;">
                Hi, ${user.firstName}!
            </span>
            <button onclick="handleLogout()" class="btn-primary logout-btn">
                Logout
            </button>
        `;
  } else {
    navButtons.innerHTML = `
            <a href="/login.html" class="btn-outline">Login</a>
            <a href="/signup.html" class="btn-primary">Sign Up</a>
        `;
  }
}

// Handle Logout
async function handleLogout() {
  try {
    await apiRequest("/logout", "POST");
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    TokenManager.remove();
    UserManager.remove();
    window.location.href = "/index.html";
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", async () => {
  // Update navigation
  updateNavigation();

  // Check page protection
  await initPageProtection();

  // Update CTAs based on auth
  updateCTAButtons();
});

// Update CTA buttons with authentication checks
function updateCTAButtons() {
  const isLoggedIn = UserManager.isLoggedIn();

  // "Get started for free" buttons
  const getStartedButtons = document.querySelectorAll(
    ".get-started-btn, a.how-btn"
  );
  getStartedButtons.forEach((btn) => {
    btn.href = "/signup.html";
  });

  // "Book your free induction" buttons
  const bookButtons = document.querySelectorAll(".book-induction-btn");
  bookButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      if (isLoggedIn) {
        window.location.href = "/contact.html";
      } else {
        sessionStorage.setItem("redirectAfterLogin", "/contact.html");
        window.location.href = "/login.html";
      }
    });
  });

  // "Contact support" button
  const contactButtons = document.querySelectorAll("a.support-btn");
  contactButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      if (isLoggedIn) {
        window.location.href = "/contact.html";
      } else {
        sessionStorage.setItem("redirectAfterLogin", "/contact.html");
        window.location.href = "/login.html";
      }
    });
  });
}

// Export functions for use in other scripts
window.AuthAPI = {
  login: async (email, password) => {
    const result = await apiRequest("/login", "POST", { email, password });
    TokenManager.set(result.access_token);
    UserManager.set(result.user);
    return result;
  },

  register: async (firstName, lastName, email, password) => {
    const result = await apiRequest("/register", "POST", {
      firstName,
      lastName,
      email,
      password,
    });
    TokenManager.set(result.access_token);
    UserManager.set(result.user);
    return result;
  },

  forgotPassword: async (email) => {
    return await apiRequest("/forgot-password", "POST", { email });
  },

  resetPassword: async (token, newPassword) => {
    return await apiRequest("/reset-password", "POST", { token, newPassword });
  },

  logout: handleLogout,
  isLoggedIn: UserManager.isLoggedIn,
  getUser: UserManager.get,
};
