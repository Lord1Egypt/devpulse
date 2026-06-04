document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.getElementById("searchBtn");
  const usernameInput = document.getElementById("usernameInput");
  const loader = document.getElementById("loader");
  const dashboard = document.getElementById("dashboard");
  
  // Dashboard fields
  const userAvatar = document.getElementById("userAvatar");
  const userName = document.getElementById("userName");
  const userLogin = document.getElementById("userLogin");
  const userBio = document.getElementById("userBio");
  const statRepos = document.getElementById("statRepos");
  const statStars = document.getElementById("statStars");
  const statForks = document.getElementById("statForks");
  const statFollowers = document.getElementById("statFollowers");
  
  // Designer fields
  const themeButtons = document.querySelectorAll(".theme-btn");
  const badgePreviewImg = document.getElementById("badgePreviewImg");
  const markdownCode = document.getElementById("markdownCode");
  const imageUrlCode = document.getElementById("imageUrlCode");
  
  const copyMdBtn = document.getElementById("copyMdBtn");
  const copyUrlBtn = document.getElementById("copyUrlBtn");

  let currentUsername = "Lord1Egypt";
  let activeTheme = "dark";

  // Check current host URL to formulate badge links automatically
  const getBaseUrl = () => {
    // If running locally without vercel dev (e.g. double-click index.html), fallback to a test or vercel URL
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://localhost:5000";
    }
    return window.location.origin;
  };

  const updateBadgeCodes = () => {
    const base = getBaseUrl();
    const badgeUrl = `${base}/api/stats?username=${currentUsername}&theme=${activeTheme}`;
    
    // Set previews
    badgePreviewImg.src = badgeUrl;
    imageUrlCode.value = badgeUrl;
    markdownCode.value = `[![DevPulse Profile Stats](${badgeUrl})](https://github.com/${currentUsername})`;
  };

  const fetchGithubStats = async (username) => {
    loader.classList.remove("hidden");
    dashboard.classList.add("hidden");
    
    try {
      // 1. Fetch Profile Details
      const pRes = await fetch(`https://api.github.com/users/${username}`);
      if (!pRes.ok) {
        throw new Error(pRes.status === 404 ? "GitHub User not found!" : "API Error fetching profile.");
      }
      const profile = await pRes.json();
      
      // 2. Fetch Repos details (Up to 100)
      const rRes = await fetch(`https://api.github.com/users/${username}/repos?per_page=100`);
      const repos = rRes.ok ? await rRes.json() : [];
      
      // Compute stats
      const totalStars = repos.reduce((sum, r) => sum + r.stargazers_count, 0);
      const totalForks = repos.reduce((sum, r) => sum + r.forks_count, 0);
      
      // Populate UI fields
      userAvatar.src = profile.avatar_url;
      userName.textContent = profile.name || profile.login;
      userLogin.textContent = `@${profile.login}`;
      userBio.textContent = profile.bio || "No bio available.";
      
      statRepos.textContent = profile.public_repos;
      statStars.textContent = totalStars;
      statForks.textContent = totalForks;
      statFollowers.textContent = profile.followers;
      
      // Show dashboard
      currentUsername = profile.login;
      updateBadgeCodes();
      
      loader.classList.add("hidden");
      dashboard.classList.remove("hidden");
      
    } catch (err) {
      loader.classList.add("hidden");
      alert(err.message || "Failed to fetch GitHub stats. Try again later.");
    }
  };

  // Search trigger
  searchBtn.addEventListener("click", () => {
    const user = usernameInput.value.trim();
    if (user) {
      fetchGithubStats(user);
    }
  });

  usernameInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      searchBtn.click();
    }
  });

  // Theme triggers
  themeButtons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      // Toggle active states
      themeButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      activeTheme = btn.dataset.themeName;
      document.body.setAttribute("data-theme", activeTheme);
      updateBadgeCodes();
    });
  });

  // Copy clipboards helpers
  const setupCopyBtn = (btn, inputField) => {
    btn.addEventListener("click", () => {
      inputField.select();
      inputField.setSelectionRange(0, 99999); // For mobile devices
      
      try {
        navigator.clipboard.writeText(inputField.value);
        const originalText = btn.textContent;
        btn.textContent = "Copied!";
        btn.style.background = "#238636";
        btn.style.color = "#ffffff";
        
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.background = "";
          btn.style.color = "";
        }, 1500);
      } catch (err) {
        alert("Failed to copy automatically. Please select the text and copy manually.");
      }
    });
  };

  setupCopyBtn(copyMdBtn, markdownCode);
  setupCopyBtn(copyUrlBtn, imageUrlCode);

  // Run initial query on page load
  fetchGithubStats(currentUsername);
});
