const socket = new WebSocket('ws://localhost:5600');
let conn_close = false;

socket.addEventListener('open', function (event) {
    console.log('Connection Established');
});

let lstGen = [];
let gen = '0';
let max = 0;
let avg = 0;
let std = 0;
let history_std = [];
let count = 0;
//выполняет то, что надо, когда состояние месса от сервера(сокета)
socket.addEventListener('message', function (event) {
    var arr = event.data.split('|');
    if (arr[0]=='stats') {
        max = Number(arr[1]).toFixed(7);
        avg = Number(arr[2]).toFixed(7);
        std = Number(arr[3]).toFixed(7);
    } else if (arr[0]=='report'){
        count+=1;
        document.getElementById('report').innerHTML = "";
        document.getElementById('report').insertAdjacentHTML('beforeend', `<h4 style="margin: 5px;">Метрики качества модели:</h4>`);
        document.getElementById('report').insertAdjacentHTML('beforeend', `<div class="report2" id="report2" style="width: 70%;">
                                                                                <p>Balanced accuracy score = ${arr[1]}</p>
                                                                                <p>Precision score = ${arr[2]}</p>
                                                                                <p>Recall score = ${arr[3]}</p>
                                                                                <p>F1 score = ${arr[4]}</p>
                                                                            </div>`);
        document.getElementById('report').insertAdjacentHTML('beforeend', `<img src="../gr${arr[5]}.png">`);
    } else {
        arr[1] = arr[1].replace(/[^a-zа-яё0-9.\s]/gi, '').split(' ');
        arr[2] = Number(arr[2].replace(/[^0-9.]/g, '')).toFixed(7);
        if (arr[0] == gen){
            if (arr[3]==1){
                lstGen.push([`<div class="fl-col" style="border-color: svet">
                            <div class="fl-col-text">
                                    <p>Gen: ${arr[0]}</p>
                                    <p>Penalty: ${arr[1][0]}</p>
                                    <p>C: ${arr[1][1]}</p>
                                    <p>MaxIter: ${arr[1][2]}</p>
                                    <p>FitnessF = ${arr[2]}</p>
                            </div>
                        </div>`, arr[2]]);
            } else {
                lstGen.push([`<div class="fl-col" style="border-color: svet">
                                <div class="fl-col-text">
                                        <p>Gen: ${arr[0]}</p>
                                        <p>N_estimators: ${arr[1][0]}</p>
                                        <p>Criterion: ${arr[1][1]}</p>
                                        <p>Max_depth: ${arr[1][2]}</p>
                                        <p>MinSamples_split: ${arr[1][3]}</p>
                                        <p>FitnessF = ${arr[2]}</p>
                                </div>
                            </div>`, arr[2]]);
            };

        } else {
            document.getElementById('wrapper').insertAdjacentHTML('beforeEnd', `<div class="f1-row" id="${gen}"></div>`);
            for (let ind of lstGen) {
                if (ind[1] >= (avg)) {
                    ind[0] = ind[0].replace("svet", "#66BF81");
                    document.getElementById(gen).insertAdjacentHTML('beforeEnd', ind[0]);
                } else if (ind[1] <= (avg)) {
                    ind[0] = ind[0].replace("svet", "#B55757");
                    document.getElementById(gen).insertAdjacentHTML('beforeEnd', ind[0]);
                } else {
                    ind[0] = ind[0].replace("svet", "#85acce");
                    document.getElementById(gen).insertAdjacentHTML('beforeEnd', ind[0]);
                };
            };
            gen = arr[0];
            lstGen = [];
            if (arr[3]==1){
                lstGen.push([`<div class="fl-col" style="border-color: svet">
                            <div class="fl-col-text">
                                    <p>Gen: ${arr[0]}</p>
                                    <p>Penalty: ${arr[1][0]}</p>
                                    <p>C: ${arr[1][1]}</p>
                                    <p>MaxIter: ${arr[1][2]}</p>
                                    <p>FitnessF = ${arr[2]}</p>
                            </div>
                        </div>`, arr[2]]);
            } else {
                lstGen.push([`<div class="fl-col" style="border-color: svet">
                                <div class="fl-col-text">
                                        <p>Gen: ${arr[0]}</p>
                                        <p>N_estimators: ${arr[1][0]}</p>
                                        <p>Criterion: ${arr[1][1]}</p>
                                        <p>Max_depth: ${arr[1][2]}</p>
                                        <p>MinSamples_split: ${arr[1][3]}</p>
                                        <p>FitnessF = ${arr[2]}</p>
                                </div>
                            </div>`, arr[2]]);
            };

            history_std.push(avg);
            if (history_std.length==3){
                if (Math.abs(Number(history_std[0])-Number(history_std[1]))<0.0001 && Math.abs(Number(history_std[1])-Number(history_std[2]))<0.0001){
                    stop();
                } else {
                    history_std.shift();
                };
            };
        };
    };

});

function go(){
    document.getElementById('wrapper').innerHTML = "";
    document.getElementById('report').innerHTML = "";
    lstGen = [];
    gen = '0';
    max = 0;
    avg = 0;
    let sel = document.getElementById("sel-select").value;
    let mate = document.getElementById("mate-select").value;
    let PC = document.getElementById("PC").value;
    let mutate = document.getElementById("mutate-select").value;
    let PM = document.getElementById("PM").value;
    let sizeP = document.getElementById("sizeP").value;
    let sizeI = document.getElementById("sizeI").value;
    let model = document.getElementById("model").value;
    socket.send('start '+JSON.stringify([new String(sel), new String(mate), new String(PC), 
        new String(mutate), new String(PM), new String(sizeP), new String(sizeI), new String(model)]));
}

const contactServer = () => {
    if (conn_close == true){
        conn_close = false;
        location.reload();
        go();
    };
    go();
};

const stop = () => {
    conn_close = true;
    socket.close();
};