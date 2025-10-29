document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("menu-toggle");
  const menu = document.getElementById("mobile-menu");
  const overlay = document.getElementById("menu-overlay");
  const scrollBtn = document.getElementById("scrollTopBtn");
  const navbar = document.getElementById("navbar");
  const hero = document.getElementById("hero");
  const heroContent = document.getElementById("heroContent");
  const progressBar = document.getElementById("progress-bar");

  /* ----- Mobile Menu ----- */
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
  toggle.addEventListener("click", () => menu.classList.contains("active") ? closeMenu() : openMenu());
  overlay.addEventListener("click", closeMenu);
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", closeMenu));

  /* ----- Scroll Progress ----- */
  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const docHeight = document.body.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = `${scrollPercent}%`;
  });

  /* ----- Navbar shrink ----- */
  window.addEventListener("scroll", () => {
    navbar.classList.toggle("scrolled", window.scrollY > 50);
  });

  /* ----- Scroll-to-top ----- */
  if (scrollBtn) {
    window.addEventListener("scroll", () => {
      scrollBtn.classList.toggle("show", window.scrollY > 300);
    });
    scrollBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  /* ----- Parallax Hero ----- */
  const bg = document.getElementById("parallax-bg");
  if (bg) {
    window.addEventListener("scroll", () => {
      bg.style.transform = `translateY(${window.scrollY * 0.4}px)`;
    });
  }

  /* ----- Hero fade-out ----- */
  if (hero && heroContent) {
    window.addEventListener("scroll", () => {
      const fadePoint = hero.offsetHeight * 0.6;
      const scrollY = window.scrollY;
      heroContent.style.opacity = Math.max(0, 1 - scrollY / fadePoint);
    });
  }

  /* ----- Cursor Reactive Glow for Footer Socials ----- */
  const socials = document.querySelectorAll(".footer-socials-bottom .social-btn");
  socials.forEach(btn => {
    btn.addEventListener("mousemove", e => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      btn.style.setProperty("--x", `${x}px`);
      btn.style.setProperty("--y", `${y}px`);
      btn.dataset.glow = true;
    });
    btn.addEventListener("mouseleave", () => {
      btn.removeAttribute("data-glow");
    });
  });
});

  /* ----- Mobile Tooltip Tap Support ----- */
  const socialButtons = document.querySelectorAll(".social-btn");

  socialButtons.forEach((btn) => {
    let tooltipVisible = false;

    btn.addEventListener("touchstart", (e) => {
      e.preventDefault(); // prevent accidental click
      tooltipVisible = !tooltipVisible;

      if (tooltipVisible) {
        btn.classList.add("show-tooltip");
        // Hide any others currently open
        socialButtons.forEach((b) => {
          if (b !== btn) b.classList.remove("show-tooltip");
        });
      } else {
        btn.classList.remove("show-tooltip");
      }
    });

    // Hide tooltip when tapping elsewhere
    document.addEventListener("touchstart", (event) => {
      if (!btn.contains(event.target)) {
        btn.classList.remove("show-tooltip");
        tooltipVisible = false;
      }
    });
  });

    /* ----- Fancy Ripple Effect on Click ----- */
  document.querySelectorAll(".social-btn, .btn-primary, .btn-outline").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      const ripple = document.createElement("span");
      ripple.classList.add("ripple");
      this.appendChild(ripple);

      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.width = ripple.style.height = size + "px";

      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      ripple.style.left = x + "px";
      ripple.style.top = y + "px";

      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });


