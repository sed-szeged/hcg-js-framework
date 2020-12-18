const fs = require('fs');
const path = require('path');

function metricCalculator(cg, threshold){
    let nodes = {};
    
    for(let node of cg.nodes){
        nodes[node.id] = node;
        nodes[node.id]['hnii'] = 0;
        nodes[node.id]['hnoi'] = 0;
        delete nodes[node.id].id;
    }
    
    for(let edge of cg.links){
        if(edge.confidence < threshold){
            continue;
        }

        nodes[edge.target].hnii++;
        nodes[edge.source].hnoi++;
    }


    return nodes;

}

function getDirectories(source){
    return fs.readdirSync(source, {withFileTypes: true})
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name);
}

const args = process.argv.slice(2);

const dirOfCgs = args[0];
const threshold = args[1];
const outDir = args[2];

for(let dir of getDirectories(dirOfCgs)){
    let cg = JSON.parse(fs.readFileSync(path.join(dirOfCgs, dir, 'eslint.json') ));
    
    let nodes = metricCalculator(cg, threshold);
    
    fs.mkdirSync(path.join(outDir, dir), { recursive: true });
    fs.writeFileSync(path.join(outDir, dir, 'eslint.json'), JSON.stringify(nodes));
    
}

