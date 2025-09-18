// Global Air Quality Monitoring Dashboard JavaScript

class AirQualityDashboard {
    constructor() {
        this.map = null;
        this.markers = [];
        this.airQualityData = [];
        this.categories = [];
        
        this.init();
    }

    async init() {
        try {
            await this.loadCategories();
            await this.loadAirQualityData();
            this.initMap();
            this.renderOverviewCards();
            this.renderTable();
            this.renderLegend();
            this.addMapMarkers();
            
            // Refresh data every 5 minutes
            setInterval(() => this.refreshData(), 300000);
        } catch (error) {
            console.error('Error initializing dashboard:', error);
            this.showError('Failed to load air quality data');
        }
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/categories');
            this.categories = await response.json();
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    async loadAirQualityData() {
        try {
            this.showLoading();
            const response = await fetch('/api/air-quality/all');
            this.airQualityData = await response.json();
            this.hideLoading();
        } catch (error) {
            console.error('Error loading air quality data:', error);
            this.hideLoading();
            throw error;
        }
    }

    initMap() {
        this.map = L.map('air-quality-map').setView([30, 0], 2);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);
    }

    addMapMarkers() {
        // Clear existing markers
        this.markers.forEach(marker => this.map.removeLayer(marker));
        this.markers = [];

        this.airQualityData.forEach(data => {
            if (!data.location || data.error) return;

            const { location, aqi, category } = data;
            const color = this.getAQIColor(aqi);
            
            const marker = L.circleMarker([location.latitude, location.longitude], {
                radius: this.getMarkerSize(aqi),
                fillColor: color,
                color: '#fff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            });

            const popupContent = `
                <div>
                    <h6><strong>${location.name}</strong></h6>
                    <div class="popup-aqi" style="color: ${color};">${aqi}</div>
                    <div class="popup-category" style="background-color: ${color};">
                        ${category.name}
                    </div>
                    <small>Dominant: ${data.dominant_pollutant}</small>
                </div>
            `;

            marker.bindPopup(popupContent);
            marker.addTo(this.map);
            this.markers.push(marker);
        });
    }

    renderOverviewCards() {
        const container = document.getElementById('overview-cards');
        container.innerHTML = '';

        this.airQualityData.forEach(data => {
            if (data.error) return;

            const card = this.createOverviewCard(data);
            container.appendChild(card);
        });
    }

    createOverviewCard(data) {
        const { location, aqi, category } = data;
        const color = this.getAQIColor(aqi);

        const cardDiv = document.createElement('div');
        cardDiv.className = 'col-lg-2 col-md-4 col-sm-6 mb-4';
        
        cardDiv.innerHTML = `
            <div class="card aqi-card h-100 fade-in" style="border-left: 4px solid ${color};">
                <div class="card-body text-center">
                    <p class="aqi-value" style="color: ${color};">${aqi}</p>
                    <p class="aqi-category" style="color: ${color};">${category.name}</p>
                    <p class="location-name">${location.name}</p>
                    <small class="text-muted">
                        <i class="fas fa-map-marker-alt"></i> ${location.country}
                    </small>
                </div>
            </div>
        `;

        return cardDiv;
    }

    renderTable() {
        const tbody = document.querySelector('#locations-table tbody');
        tbody.innerHTML = '';

        this.airQualityData.forEach(data => {
            if (data.error) return;

            const row = document.createElement('tr');
            const color = this.getAQIColor(data.aqi);
            const timestamp = new Date(data.timestamp).toLocaleString();

            row.innerHTML = `
                <td>
                    <strong>${data.location.name}</strong><br>
                    <small class="text-muted">${data.location.country}</small>
                </td>
                <td>
                    <span class="aqi-badge" style="background-color: ${color};">
                        ${data.aqi}
                    </span>
                </td>
                <td>
                    <span class="category-badge" style="background-color: ${color};">
                        ${data.category.name}
                    </span>
                </td>
                <td>${data.dominant_pollutant}</td>
                <td>
                    <small>${timestamp}</small>
                </td>
            `;

            tbody.appendChild(row);
        });
    }

    renderLegend() {
        const container = document.getElementById('aqi-legend');
        container.innerHTML = '';

        this.categories.forEach(category => {
            const item = document.createElement('div');
            item.className = 'aqi-legend-item';
            
            item.innerHTML = `
                <div class="legend-color" style="background-color: ${category.color};"></div>
                <div class="legend-text">
                    <div><strong>${category.name}</strong></div>
                </div>
                <div class="legend-range">
                    <small>${category.min_aqi}-${category.max_aqi}</small>
                </div>
            `;

            container.appendChild(item);
        });
    }

    getAQIColor(aqi) {
        for (const category of this.categories) {
            if (aqi >= category.min_aqi && aqi <= category.max_aqi) {
                return category.color;
            }
        }
        return '#7E0023'; // Default to hazardous color
    }

    getMarkerSize(aqi) {
        if (aqi <= 50) return 8;
        if (aqi <= 100) return 12;
        if (aqi <= 150) return 16;
        if (aqi <= 200) return 20;
        if (aqi <= 300) return 24;
        return 28;
    }

    async refreshData() {
        try {
            await this.loadAirQualityData();
            this.renderOverviewCards();
            this.renderTable();
            this.addMapMarkers();
            
            // Show brief notification
            this.showNotification('Data refreshed', 'success');
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showNotification('Failed to refresh data', 'error');
        }
    }

    showLoading() {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    hideLoading() {
        const modalElement = document.getElementById('loadingModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
            modal.hide();
        }
    }

    showError(message) {
        const container = document.getElementById('overview-cards');
        container.innerHTML = `
            <div class="col-12">
                <div class="error-card">
                    <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                    <h4>Error Loading Data</h4>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-refresh"></i> Retry
                    </button>
                </div>
            </div>
        `;
    }

    showNotification(message, type = 'info') {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'} me-2"></i>
                ${message}
            </div>
        `;

        document.body.appendChild(toast);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AirQualityDashboard();
});

// Add smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});