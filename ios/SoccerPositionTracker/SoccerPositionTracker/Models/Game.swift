//
//  Game.swift
//  SoccerPositionTracker
//
//  Created by Logan Patino on 2/18/26.
//

import Foundation

struct Game: Codable {
    let id: UUID
    let position: String
    let my_team_score: Int?
    let opponent_score: Int?
    let field_id: Int
}
