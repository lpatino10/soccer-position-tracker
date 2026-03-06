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
                            fieldId: selectedFieldId!
                        )
                    }
                    isGameStarted = true
                }
                .disabled(selectedFieldId == nil)
                .buttonStyle(.glassProminent)
            }
            .padding()
            .navigationDestination(isPresented: $isGameFinished) {
                VStack {
                    HStack {
                        Text("Final Score")
                            .font(.title3)
                        Spacer()
                    }
                    
                    HStack {
                        Text("My Team:")
                            .font(.callout)
                        Stepper("\(myTeamScore)", value: $myTeamScore)
                            .font(.headline)
                    }
                    
                    HStack {
                        Text("Opponent:")
                            .font(.callout)
                        Stepper("\(opponentScore)", value: $opponentScore)
                            .font(.headline)
                    }
                    
                    Divider().padding(EdgeInsets(top: 12, leading: 0, bottom: 12, trailing: 0))
                    
                    LabeledContent {
                        TextField("Center mid", text: $position)
                            .multilineTextAlignment(.trailing)
                    } label: {
                        Text("Position")
                            .font(.title3)
                    }
                    
                    Spacer()
                    
                    Button("Save") {
                        Task {
                            print(newGameId)

                            try? await MySupabaseClient.shared.updateGame(
                                id: newGameId,
                                position: position,
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
                    .disabled(position.isEmpty)
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

            guard let fields = try? await MySupabaseClient.shared.listFields() else { return }
            fieldOptions = fields
            selectedFieldId = fields[0].id
        }
    }
}

#Preview {
    ContentView()
}
