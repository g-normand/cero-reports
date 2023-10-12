import csvtojson from "csvtojson";
import fs from "fs";

const sp = await csvtojson.csv().fromFile("src/assets/obs_list.csv")


const sp_region = sp.map(s => {
    return {
        speciesCode: s.speciesCode,
        comName: s.comName,
        locId: s.locId,
        locName: s.locName,
        howMany: s.howMany,
        locName: s.locName,
        obsDt: s.obsDt,
        lat: s.lat,
        lng: s.lng,
        cero_report: s.cero_report,
        altitude: s.altitude,
        subId: s.subId,
        userDisplayName: s.userDisplayName,
    }
})

await fs.writeFileSync('src/assets/obs_list.json', JSON.stringify(sp_region));