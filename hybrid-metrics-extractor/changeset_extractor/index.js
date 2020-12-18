const fs = require('fs');
const loader = require('csv-load-sync');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;


function findInCSV(csv, needle){
    return csv.filter((item) =>{
        return item.Path === needle.Path && item.LongName === needle.LongName;
    });
}

function findByPos(csv, needle){
    return csv.filter((item) =>{
        return item.Path === needle.Path && item.Line === needle.Line;
    });
}

function appendHNiiHNoi(callgraph, row){
    for(const property in callgraph){
        let pos = callgraph[property].pos.split(":");
        
        if(pos[0] == row.Path && pos[1] == row.Line){
            row['HNOI'] = callgraph[property]['hnoi'];
            row['HNII'] = callgraph[property]['hnii'];
            return row;
        }
    }

    return null;
}

let latest_analysis_csv = args[0]; // Relative path to the chronologically latest SourceMeter analysis result (function.csv). E.g.: '../sm_results/Bug-79-fix-Function.csv'
let buggy_csv = args[1]; // Relative path to the CSV containing buggy entries. E.g.: '../buggy_csv/hybrid_0_00.csv'
let callgraph_json = args[2]; // Relative path to the JSON containing the nodes with hnii and hnoi values (result of HNII HNOI counter). E.g.: '../hnii_hnoi_cg/0_00/eslint.json'
let output = args[3];

let sm_csv = loader(latest_analysis_csv);
buggy_csv = loader(buggy_csv);
let rawCallgraph = fs.readFileSync(callgraph_json);
let callgraph = JSON.parse(rawCallgraph);


let counter = 0;
sm_csv.forEach((row) => {
    let res = findInCSV(buggy_csv, row);
    if(res.length == 0){
        res = findByPos(buggy_csv, row);
    }

	// Not yet in buggy
    if(res.length == 0){
        // search for hnii hnoi in json
        let newRecord = appendHNiiHNoi(callgraph, row);
        if(newRecord != null){
            newRecord['Bug'] = 0;
            buggy_csv.push(newRecord);
        }
    }
    counter += res.length;
});

let header = [];
for(let key in buggy_csv[0]){
    header.push({id: key, title: key});
}

const csvWriter = createCsvWriter({
    path: output,
    header: header
  });

csvWriter.writeRecords(buggy_csv).then(()=> console.log('The CSV file was written successfully'));

