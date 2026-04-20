document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('travelForm');
    if (!form) return;

    // Handle Chip Selection
    const chips = document.querySelectorAll('.chip');
    let selectedInterests = ['culture', 'food']; // Default active

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chip.classList.toggle('active');
            const val = chip.getAttribute('data-value');
            if (selectedInterests.includes(val)) {
                selectedInterests = selectedInterests.filter(i => i !== val);
            } else {
                selectedInterests.push(val);
            }
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI State loading
        const btn = document.getElementById('generateBtn');
        const btnText = btn.querySelector('.btn-text');
        const loader = document.getElementById('loaderContainer');
        const percentSpan = document.getElementById('loadingPercentage');
        
        btnText.textContent = "Architecting Plan...";
        loader.classList.remove('hidden');
        btn.disabled = true;
        
        let percent = 0;
        percentSpan.textContent = '0%';
        const progressInterval = setInterval(() => {
            if (percent < 95) {
                percent += Math.floor(Math.random() * 12) + 1; // Increment by 1-12
                if (percent > 95) percent = 95;
                percentSpan.textContent = percent + '%';
            }
        }, 400);

        // Gather Data
        const payload = {
            destination: document.getElementById('dest').value,
            days: document.getElementById('days').value,
            interests: selectedInterests.length > 0 ? selectedInterests.join(', ') : 'general',
            budget: document.getElementById('budget').value,
            email: document.getElementById('email').value
        };

        try {
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await response.json();
            
            clearInterval(progressInterval);
            percentSpan.textContent = '100%';
            
            if (result.status === 'success') {
                renderTimeline(result.data);
            } else {
                alert("An error occurred planning your trip.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Connection error.");
            clearInterval(progressInterval);
        } finally {
            // slight delay to let user see 100%
            setTimeout(() => {
                btnText.textContent = "Generate Smart Itinerary 🚀";
                loader.classList.add('hidden');
                btn.disabled = false;
            }, 400);
        }
    });

    function renderTimeline(data) {
        const resultsArea = document.getElementById('resultsArea');
        const timeline = document.getElementById('timeline');
        timeline.innerHTML = '';
        resultsArea.classList.remove('hidden');

        // Smooth scroll to results
        resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

        data.days_list.forEach((dayPlan, index) => {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'timeline-day';
            dayDiv.innerHTML = `<h3 class="day-title">Day ${index + 1}</h3>`;

            const slots = ["Morning", "Lunch", "Afternoon", "Evening"];
            slots.forEach(slot => {
                if (dayPlan[slot]) {
                    const activity = dayPlan[slot];
                    const card = document.createElement('div');
                    card.className = 'slot-card';
                    
                    let metaHTML = `<span title="Rating">⭐ ${activity.rating}</span>`;
                    
                    if (activity.weather) {
                        metaHTML += `<span>🌤 ${activity.weather.condition} (${activity.weather.temperature}°C)</span>`;
                        if (activity.weather.air_quality) {
                            metaHTML += `<span>🍃 AQI: ${activity.weather.air_quality.aqi} (${activity.weather.air_quality.category})</span>`;
                        }
                    }
                    if (activity.crowd) {
                        let icon = activity.crowd.status === "Very Crowded" ? "🚦" : "👥";
                        metaHTML += `<span>${icon} ${activity.crowd.status}</span>`;
                    }
                    if (activity.traffic) {
                        metaHTML += `<span>🚗 Traffic: ${activity.traffic.traffic_level} (${activity.traffic.estimated_time_mins}m)</span>`;
                        if (activity.traffic.alert) {
                            metaHTML += `<span class="alert">⚠️ Alert: ${activity.traffic.alert}</span>`;
                        }
                    }

                    card.innerHTML = `
                        <div class="slot-name">${slot}</div>
                        <a href="${activity.map_url}" target="_blank" class="place-name" style="color: inherit; text-decoration: none;">
                            ${activity.place} <span style="font-size: 0.8rem;">🔗</span>
                        </a>
                        ${activity.summary ? `<div class="summary-text" style="font-size:0.85rem; color:#cbd5e1; margin-top:5px; margin-bottom:10px; font-style:italic;">${activity.summary}</div>` : ''}
                        <div class="meta-info">${metaHTML}</div>
                    `;
                    dayDiv.appendChild(card);
                }
            });
            
            timeline.appendChild(dayDiv);
        });
    }
});
