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
    private let backgroundActivity = CLBackgroundActivitySession()
    
    func requestUserAuthorization() async throws {
        if locationManager.authorizationStatus == .notDetermined || locationManager.authorizationStatus == .authorizedWhenInUse {
            locationManager.requestAlwaysAuthorization()
            locationManager.allowsBackgroundLocationUpdates = true
        }
        
        if (locationManager.authorizationStatus == .authorizedAlways) {
            print("ALWAYS AUTHORIZED")
        }
    }
 
    func startCurrentLocationUpdates(gameId: UUID) async throws {
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
        backgroundActivity.invalidate()
    }
}
