package com.example.evroutes.data.model;


data class ChargingStationRequest(
        val name: String,
        val latitude: Double,
        val longtitude: Double,
        val connection_type: String,
        val power_kw: Int
)

// Ответ со списком зарядных станций
data class ChargingStationsResponse(
        val stations: List<ChargingStation>
)

// Модель зарядной станции
data class ChargingStation(
        val id: String,
        val name: String,
        val latitude: Double,
        val longitude: Double,
        val address: String,
        val connectorTypes: List<String>,
        val power: Int, // кВт
        val isAvailable: Boolean,
        val price: Double,
        val openingHours: String,
        val rating: Double
)

data class RouteRequest(
        val fromLatitude: Double,
        val fromLongitude: Double,
        val toLatitude: Double,
        val toLongitude: Double,
        val batteryLevel: Int, // процент заряда
        val vehicleRange: Int // запас хода в км
)

// Оптимизированный маршрут
data class OptimizedRoute(
        val totalDistance: Double, // км
        val estimatedTime: Int, // минуты
        val waypoints: List<RouteWaypoint>,
        val chargingStops: List<ChargingStop>
)

// Точка маршрута
data class RouteWaypoint(
        val latitude: Double,
        val longitude: Double,
        val distanceFromStart: Double, // км от начала маршрута
        val estimatedTimeFromStart: Int // минуты от начала маршрута
)

// Остановка для зарядки
data class ChargingStop(
        val station: ChargingStation,
        val arrivalBatteryLevel: Int, // процент заряда при прибытии
        val recommendedChargingTime: Int, // минуты
        val departureBatteryLevel: Int // процент заряда при отъезде
)