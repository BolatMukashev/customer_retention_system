// ===== Mobile Menu =====
const mobileToggle = document.getElementById('mobileToggle');
const mainNav = document.getElementById('mainNav');

if (mobileToggle && mainNav) {
    mobileToggle.addEventListener('click', () => {
        mobileToggle.classList.toggle('active');
        mainNav.classList.toggle('active');
        document.body.style.overflow = mainNav.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu on link click
    mainNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileToggle.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
}

// ===== Header Scroll Effect =====
const header = document.getElementById('header');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});

// ===== Scroll Reveal =====
const revealElements = document.querySelectorAll('[data-reveal]');

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            revealObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

revealElements.forEach(el => revealObserver.observe(el));

// ===== FAQ Accordion =====
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');

    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');

        // Close all
        faqItems.forEach(i => i.classList.remove('active'));

        // Open clicked if wasn't active
        if (!isActive) {
            item.classList.add('active');
        }
    });
});

// ===== Animated Counters =====
const counters = document.querySelectorAll('[data-count]');

const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseFloat(el.dataset.count);
            const isDecimal = target % 1 !== 0;
            const duration = 2000;
            const startTime = performance.now();

            const updateCount = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Ease out quart
                const ease = 1 - Math.pow(1 - progress, 4);
                const current = target * ease;

                if (isDecimal) {
                    el.textContent = current.toFixed(1);
                } else {
                    el.textContent = Math.floor(current);
                }

                if (progress < 1) {
                    requestAnimationFrame(updateCount);
                } else {
                    if (isDecimal) {
                        el.textContent = target.toFixed(1);
                    } else {
                        el.textContent = target;
                    }
                }
            };

            requestAnimationFrame(updateCount);
            countObserver.unobserve(el);
        }
    });
}, { threshold: 0.5 });

counters.forEach(counter => countObserver.observe(counter));

// ===== Smooth Scroll for Anchor Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;

        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Parallax Effect for Hero Orbs =====
const orbs = document.querySelectorAll('.gradient-orb');

window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;

    orbs.forEach((orb, index) => {
        const speed = 0.05 + (index * 0.02);
        orb.style.transform = `translateY(${scrollY * speed}px)`;
    });
});

// ===== Dashboard Card Hover Effect =====
const dashboardCard = document.querySelector('.dashboard-card');
if (dashboardCard) {
    dashboardCard.addEventListener('mouseenter', () => {
        dashboardCard.style.animationPlayState = 'paused';
    });

    dashboardCard.addEventListener('mouseleave', () => {
        dashboardCard.style.animationPlayState = 'running';
    });
}