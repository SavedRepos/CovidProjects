//
//  WorldPopulation.swift
//  C19Graphs
//
//  Created by Paul Hart on 2020-12-27.
//

// Input csv layout
// - Country,
// - Province,
// - Combined_Key,
// - Population

import Foundation

class WorldPop {
    var countryRegion: String = ""
    var provinceState: String = ""
    var combinedKey: String = ""
    var population: Float = 0.0
}
