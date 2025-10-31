// =======================================
// USIU G6 SaaS Website Main Script
// =======================================

document.addEventListener("DOMContentLoaded", () => {

  // --- Element references ---
  const toggle = document.getElementById("menu-toggle");
  const menu = document.getElementById("mobile-menu");
  const overlay = document.getElementById("menu-overlay");
  const scrollBtn = document.getElementById("scrollTopBtn");
  const navbar = document.getElementById("navbar");
  const hero = document.getElementById("hero");
  const heroContent = document.getElementById("heroContent");
  const progressBar = document.getElementById("progress-bar");

  // ================================
  // 1. MOBILE MENU TOGGLE & OVERLAY
  // ================================
  const closeMenu = () => {
    menu.classList.remove("active");
    overlay.classList.remove("active");
    toggle.classList.remove("active");
    toggle.setAttribute("aria-expanded", "false");
  };

  const openMenu = () => {
    menu.classList.add("active");
    overlay.classList.add("active");
    toggle.classList.add("active");
    toggle.setAttribute("aria-expanded", "true");
  };

  // Handle menu toggle clicks
  toggle.addEventListener("click", () => {
    const isOpen = menu.classList.contains("active");
    isOpen ? closeMenu() : openMenu();
  });

  // Close when overlay or link clicked
  overlay.addEventListener("click", closeMenu);
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", closeMenu));


  // ================================
  // 2. STICKY NAVBAR EFFECT
  // ================================
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) navbar.classList.add("scrolled");
    else navbar.classList.remove("scrolled");
  });


  // ================================
  // 3. SCROLL PROGRESS BAR
  // ================================
  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const docHeight = document.body.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = `${scrollPercent}%`;
  });


  // ================================
  // 4. SCROLL-TO-TOP BUTTON
  // ================================
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) scrollBtn.classList.add("show");
    else scrollBtn.classList.remove("show");
  });

  scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });


  // ================================
  // 5. HERO PARALLAX EFFECT
  // ================================
  window.addEventListener("scroll", () => {
    const bg = document.getElementById("parallax-bg");
    if (bg) {
      const scrollY = window.scrollY;
      bg.style.transform = `translateY(${scrollY * 0.4}px)`;
    }
  });


    // ================================
  // 6. HERO TEXT FADE ON SCROLL (capped)
  // ================================
  window.addEventListener("scroll", () => {
    if (hero && heroContent) {
      const heroHeight = hero.offsetHeight;
      const scrollY = window.scrollY;
      const fadePoint = heroHeight * 0.6;
      if (scrollY < fadePoint) {
        const opacity = Math.max(0.75, 1 - scrollY / fadePoint); // don't drop below 0.75
        heroContent.style.opacity = opacity;
        heroContent.style.transform = `translateY(${Math.min(14, scrollY * 0.12)}px)`; // gentle shift only
      } else {
        heroContent.style.opacity = 0.75;
      }
    }
  });



  // ================================
  // 7. TOOLTIP SUPPORT FOR MOBILE
  // ================================
  const socialButtons = document.querySelectorAll(".social-btn");

  socialButtons.forEach((btn) => {
    let tooltipVisible = false;

    // Show tooltip on tap
    btn.addEventListener("touchstart", (e) => {
      e.preventDefault(); // avoid accidental click
      tooltipVisible = !tooltipVisible;

      if (tooltipVisible) {
        btn.classList.add("show-tooltip");
        // Hide all other open tooltips
        socialButtons.forEach((b) => {
          if (b !== btn) b.classList.remove("show-tooltip");
        });
      } else {
        btn.classList.remove("show-tooltip");
      }
    });

    // Hide tooltip when tapping anywhere else
    document.addEventListener("touchstart", (event) => {
      if (!btn.contains(event.target)) {
        btn.classList.remove("show-tooltip");
        tooltipVisible = false;
      }
    });
  });


  // ================================
  // 8. RIPPLE CLICK ANIMATION
  // ================================
  document.querySelectorAll(".social-btn, .btn-primary, .btn-outline").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      // Create ripple span
      const ripple = document.createElement("span");
      ripple.classList.add("ripple");
      this.appendChild(ripple);

      // Calculate position and size
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.width = ripple.style.height = size + "px";

      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      ripple.style.left = x + "px";
      ripple.style.top = y + "px";

      // Remove ripple after animation
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });



  // ================================
  // 9. SIMPLE DEMO LOGIN HANDLER ... (To be deleted)
  // ================================
  (function setupDemoLogin() {
    const isLoginPage = window.location.pathname.endsWith("/login.html") || window.location.pathname.endsWith("login.html");
    if (!isLoginPage) return;

    const authCard = document.querySelector(".auth-card") || document.querySelector(".auth-form");
    const form = authCard ? authCard.querySelector("form") : null;
    if (!form) return;

    const showAlert = (message, type) => {
      if (!authCard) return;
      // remove existing alerts
      authCard.querySelectorAll('.alert').forEach(el => el.remove());
      const div = document.createElement('div');
      div.className = `alert ${type === 'success' ? 'alert-success' : 'alert-error'}`;
      div.textContent = message;
      authCard.appendChild(div);
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = (form.querySelector('#email') || {}).value || '';
      const password = (form.querySelector('#password') || {}).value || '';
      if (!email || !password) {
        showAlert('Please provide both email and password.', 'error');
        return;
      }
      try {
        const res = await fetch('assets/data/users.json', { cache: 'no-store' });
        const users = await res.json();
        const found = (users || []).find(u => (u.email || '').toLowerCase() === email.toLowerCase() && (u.password || '') === password);
        if (!found) {
          showAlert('Invalid email or password. Try again.', 'error');
          return;
        }
        // Store demo session
        const session = { id: found.id, email: found.email, firstName: found.firstName, lastName: found.lastName, role: found.role, ts: Date.now() };
        localStorage.setItem('g6_session', JSON.stringify(session));
        showAlert('Login successful! Redirecting…', 'success');
        const params = new URLSearchParams(window.location.search);
        const next = params.get('next') || 'index.html';
        setTimeout(() => { window.location.href = next; }, 1200);
      } catch (err) {
        showAlert('Unable to sign in right now. Please try again later.', 'error');
      }
    });
  })();

  //  


});

    // ================================
  // 9. HERO PARTICLE GLOW BACKGROUND
  // ================================
  const canvas = document.getElementById("heroCanvas");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let particles = [];
    const colors = [
      "rgba(59,130,246,0.40)",  // blue
      "rgba(30,58,138,0.30)",   // dark blue
      "rgba(147,197,253,0.35)"  // light blue
    ];
    const numParticles = 25;
    let width, height;

    function resizeCanvas() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    class Particle {
      constructor() { this.reset(); }
      reset() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.radius = Math.random() * 80 + 30;
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.vx = (Math.random() - 0.5) * 0.3;
        this.vy = (Math.random() - 0.5) * 0.3;
      }
      update() {
        this.x += this.vx; this.y += this.vy;
        if (this.x < -120 || this.x > width + 120 || this.y < -120 || this.y > height + 120) this.reset();
      }
      draw() {
        ctx.beginPath();
        const g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius);
        g.addColorStop(0, this.color);
        g.addColorStop(1, "transparent");
        ctx.fillStyle = g;
        ctx.fillRect(this.x - this.radius, this.y - this.radius, this.radius * 2, this.radius * 2);
      }
    }

    function initParticles() { particles = Array.from({ length: numParticles }, () => new Particle()); }
    function animateParticles() {
      ctx.clearRect(0, 0, width, height);
      particles.forEach(p => { p.update(); p.draw(); });
      requestAnimationFrame(animateParticles);
    }
    initParticles(); animateParticles();
  }

    // ================================
  // 10. HERO SCROLL REVEAL ANIMATION
  // ================================
  const heroObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
        }
      });
    },
    { threshold: 0.3 }
  );

  const heroSection = document.querySelector(".hero-grid");
  if (heroSection) heroObserver.observe(heroSection);

    // ================================
  // 11. HERO IMAGE PARALLAX MOTION
  // ================================
  const heroImg = document.querySelector(".hero-image img");

  if (heroImg) {
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    // Subtle mouse move parallax (desktop only)
    window.addEventListener("mousemove", (e) => {
      if (window.innerWidth > 960) {
        mouseX = (e.clientX / window.innerWidth - 0.5) * 30; // horizontal sway
        mouseY = (e.clientY / window.innerHeight - 0.5) * 30; // vertical sway
      }
    });

    // Scroll-based depth parallax
    window.addEventListener("scroll", () => {
      if (window.innerWidth > 960) {
        const scrollY = window.scrollY;
        const translateY = scrollY * 0.15; // soft upward shift
        heroImg.style.transform = `translate(${targetX}px, ${translateY}px) scale(1.03)`;
      }
    });

    // Smooth interpolation for mouse motion
    function animateParallax() {
      targetX += (mouseX - targetX) * 0.05;
      targetY += (mouseY - targetY) * 0.05;

      if (window.innerWidth > 960) {
        heroImg.style.transform = `translate(${targetX}px, ${targetY * 0.2}px) scale(1.03)`;
            // Optional: dynamic shadow intensity based on mouse movement
    function updateShadow() {
      const intensity = Math.min(0.4, Math.abs(mouseX) / 60);
      heroImg.style.filter = `drop-shadow(${mouseX * 0.2}px ${mouseY * 0.2}px 20px rgba(30,58,138,${intensity}))`;
      requestAnimationFrame(updateShadow);
    }
    updateShadow();

      } else {
        heroImg.style.transform = `translateY(0)`;
      }

      requestAnimationFrame(animateParallax);
    }

    animateParallax();
  }



