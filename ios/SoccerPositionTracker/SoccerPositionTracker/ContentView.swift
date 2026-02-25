//
//  ContentView.swift
//  SoccerPositionTracker
//
//  Created by Logan Patino on 2/9/26.
//

import SwiftUI

struct ContentView: View {
    @State var locationManager = LocationManager()
    @State private var path = NavigationPath()

    @State private var newGameId = UUID()
    @State private var isGameStarted = false
    @State private var isGameFinished = false

    @State var fieldOptions: [PlayingField] = []
    @State var position: String = ""
    @State var selectedFieldId: PlayingField.ID?
    @State var myTeamScore: Int = 0
    @State var opponentScore: Int = 0
    
    var body: some View {
        NavigationStack(path: $path) {
            VStack {
                Text("New Game")
                    .font(.title)
                
                TextField("Position", text: $position)
                
                if selectedFieldId != nil {
                    LabeledContent {
                        Picker("Field", selection: $selectedFieldId) {
                            ForEach(fieldOptions) { playingField in
                                Text("\(playingField.name)")
                                    .tag(playingField.id)
                            }
                        }
                    } label: {
                        Text("Field")
                    }
                }
                
                Spacer()
                
                Button("Start Game") {
                    Task {
                        try? await MySupabaseClient.shared.createNewGame(
                            id: newGameId,
                            position: position,
                            fieldId: selectedFieldId!
                        )
                    }
                    isGameStarted = true
                }
                .disabled(position.isEmpty || selectedFieldId == nil)
                .buttonStyle(.glassProminent)
            }
            .padding()
            .navigationDestination(isPresented: $isGameFinished) {
                VStack {
                    Text("Final Score")
                        .font(.title)
                    
                    HStack {
                        Text("My Team")
                        Stepper("\(myTeamScore)", value: $myTeamScore)
                    }
                    
                    HStack {
                        Text("Opponent")
                        Stepper("\(opponentScore)", value: $opponentScore)
                    }
                    
                    Spacer()
                    
                    Button("Save") {
                        Task {
                            print(newGameId)

                            try? await MySupabaseClient.shared.updateGameScore(
                                id: newGameId,
                                myTeamScore: myTeamScore,
                                opponentScore: opponentScore
                            )
                            
                            newGameId = UUID()
                        }
                        
                        isGameStarted = false
                        isGameFinished = false
                        position = ""
                        path = NavigationPath()
                    }
                    .buttonStyle(.glassProminent)
                }
                .padding()
                .navigationBarBackButtonHidden()
            }
            .navigationDestination(isPresented: $isGameStarted) {
                VStack {
                    Text("Game in progress...")
                        .padding(.top, 64)
                    Spacer()
                    Button("End Game") {
                        isGameFinished = true
                        locationManager.stopTrackingLocation()
                    }
                    .buttonStyle(.glassProminent)
                }
                .padding()
                .navigationBarBackButtonHidden()
                .task {
                    try? await locationManager.startCurrentLocationUpdates(gameId: newGameId)
                }
            }
            
        }
        .task {
            try? await locationManager.requestUserAuthorization()
        }
        .task {
            guard let fields = try? await MySupabaseClient.shared.listFields() else { return }
            fieldOptions = fields
            selectedFieldId = fields[0].id
        }
    }
}

#Preview {
    ContentView()
}
