//
//  LocationManager.swift
//  SoccerPositionTracker
//
//  Created by Logan Patino on 2/17/26.
//

import Foundation
import CoreLocation

@Observable
final class LocationManager {
    private let locationManager = CLLocationManager()
    
    func requestUserAuthorization() async throws {
        locationManager.requestWhenInUseAuthorization()
    }
 
    func startCurrentLocationUpdates(gameId: UUID) async throws {
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.startUpdatingLocation()

        for try await locationUpdate in CLLocationUpdate.liveUpdates(.fitness) {
            if let newLocation = locationUpdate.location {
                Task {
                    try? await MySupabaseClient.shared.sendLocation(gameId: gameId, lat: newLocation.coordinate.latitude, lng: newLocation.coordinate.longitude)
                }
            }
        }
    }
    
    func stopTrackingLocation() {
        locationManager.stopUpdatingLocation()
    }
}
