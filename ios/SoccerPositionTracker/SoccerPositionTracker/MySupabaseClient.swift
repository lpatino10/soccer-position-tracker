//
//  MySupabaseClient.swift
//  SoccerPositionTracker
//
//  Created by Logan Patino on 2/18/26.
//

import Foundation
import Supabase

final class MySupabaseClient {
    static let shared = MySupabaseClient()
    
    let client: SupabaseClient
    
    private init() {
        client = SupabaseClient(
            supabaseURL: URL(string: "https://paugmeoshsaakpmuwsoo.supabase.co")!,
            supabaseKey: "sb_publishable_YW4rIYbyDM9k6Rlisuk_yw_YSbt9p2V",
            options: SupabaseClientOptions(
                auth: .init(
                    emitLocalSessionAsInitialSession: true
                )
            )
        )
    }
    
    func listFields() async throws -> [PlayingField] {
        let fields: [PlayingField] = try await client.from("Field").select().execute().value
        return fields
    }
    
    func createNewGame(id: UUID, position: String, fieldId: Int) async throws {
        try await client
            .from("Game")
            .insert(Game(id: id, position: position, my_team_score: nil, opponent_score: nil, field_id: fieldId))
            .execute()
    }
    
    func updateGameScore(id: UUID, myTeamScore: Int, opponentScore: Int) async throws {
        try await client
            .from("Game")
            .update(["my_team_score": myTeamScore, "opponent_score": opponentScore])
            .eq("id", value: id.uuidString.lowercased())
            .execute()
    }
    
    func sendLocation(gameId: UUID, lat: Double, lng: Double) async throws {
        // TODO: Avoid sending to DB if location is out of bounds.
        try await client
            .from("TrackingEvent")
            .insert(TrackingEvent(timestamp: Date().ISO8601Format(), lat: lat, lng: lng, game_id: gameId))
            .execute()
    }
}
