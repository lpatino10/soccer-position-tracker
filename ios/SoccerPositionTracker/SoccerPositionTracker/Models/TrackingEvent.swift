//
//  TrackingEvent.swift
//  SoccerPositionTracker
//
//  Created by Logan Patino on 2/18/26.
//

import Foundation

struct TrackingEvent: Encodable {
    let timestamp: String
    let lat: Double
    let lng: Double
    let game_id: UUID
}
