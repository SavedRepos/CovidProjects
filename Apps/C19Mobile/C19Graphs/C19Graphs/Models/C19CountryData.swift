//
//  C19CountryData.swift
//  C19Graphs
//
//  Created by Paul Hart on 2020-12-27.
//

/*  Input csv layout
 *  - Province_State,
 *  - Country_Region,
 *  - Lat,
 *  - Long,
 *  - Date,
 *  - Confirmed,
 *  - Deaths,
 *  - Combined_Key,
 *  - ConfirmedNew,
 *  - DeathsNew,
 *  - ConfirmedNewMean,
 *  - DeathsNewMean,
 *  - Population
 */

import Foundation

class AreaDetails {
    var url: String = ""
    var provinceState: String = ""
    var countryRegion: String = ""
    var lat: String = ""
    var long: String = ""
    var combinedKey: String = ""
    var population: Float = 0.0
    var date: [String] = []
    var confirmed: [Float] = []
    var confirmedNew: [Float] = []
    var confirmedNewMean: [Float] = []
    var deaths: [Float] = []
    var deathsNew: [Float] = []
    var deathsNewMean: [Float] = []
    
    var lock: NSLock? = nil
    public var code: String

    init(code: String, sync: Bool = false) {
        // Fetch data from Github

        self.code = code
        
        //    if sync {
        //        lock = NSLock()
        //    }
        //    fetchNewSnapshot()
        //    if sync {
        //        lock?.lock ()
        //    }

        // Build this object
    }

    //public func fetchNewSnapshot (session: URLSession? = nil){
    //    let url = URL(string: "https://github.com/jpaulhart/Plague-2020/blob/master/Data/CSVFiles/\(code).csv")!
    //    let url = URL(string: "https://tirania.org/covid-data/\(code)")!
    //    var request = URLRequest(url: url)
    //    request.httpMethod = "GET"
    //
    //    let task = (session ?? URLSession.shared).dataTask(with: request, completionHandler: receivedData(data:response:error:))
    //
    //    task.resume()
    //}
}

///// Creates an UpdatableStat with a `code` that reprensents one of the known locations that we have statistics for
//public init (code: String, sync: Bool = false)
//{
//    self.code = code
//    self.tl = globalData.globals [code]
//
//    if let existing = IndividualSnapshot.tryLoadCache(name: code) {
////            var current = Calendar.current
////            var components = current.dateComponents(in: current.timeZone, from: Date ())
//
//        // If it is fresh enough, no need to download
//        if existing.time + TimeInterval(24*60*60) > Date () {
//            self.stat = makeStat(trackedLocation: self.tl, snapshot: existing.snapshot, date: existing.time)
//            return
//        }
//    }
//    if sync {
//        lock = NSLock()
//    }
//    fetchNewSnapshot()
//    if sync {
//        lock?.lock ()
//    }
//}


