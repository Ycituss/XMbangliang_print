function submitForm() {
    document.getElementById('myForm').submit();
}

function close_ip1() {
    fetch('/ban_ip1')
    .then(response => response.text())
    .then(data => {
        const elementToRemove = document.getElementById('ip-1');
        if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
        // document.getElementById('signature').innerText = data
        console.log(data)
    })
    updateClientCount();
}

function close_ip2() {
    fetch('/ban_ip2')
   .then(response => response.text())
   .then(data => {
        const elementToRemove = document.getElementById('ip-2');
        if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
        // document.getElementById('signature').innerText = data
        console.log(data)
    })
    updateClientCount();
}

function close_ip3() {
    fetch('/ban_ip3')
   .then(response => response.text())
   .then(data => {
        const elementToRemove = document.getElementById('ip-3');
        if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
        // document.getElementById('signature').innerText = data
        console.log(data)
    })
    updateClientCount();
}

function close_ip4() {
    fetch('/ban_ip4')
   .then(response => response.text())
   .then(data => {
        const elementToRemove = document.getElementById('ip-4');
        if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
        // document.getElementById('signature').innerText = data
        console.log(data)
    })
    updateClientCount();
}

function close_ip5() {
    fetch('/ban_ip5')
   .then(response => response.text())
   .then(data => {
        const elementToRemove = document.getElementById('ip-5');
        if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
        // document.getElementById('signature').innerText = data
        console.log(data)
    })
    updateClientCount();
}

function close_ip6() {
    fetch('/ban_ip6')
   .then(response => response.text())
   .then(data => {
        const elementToRemove = document.getElementById('ip-6');
        if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
        // document.getElementById('signature').innerText = data
        console.log(data)
    })
    updateClientCount();
}

function updateClientCount() {
    fetch('/get_ip_list')
       .then(response => response.text())
       .then(data => {
            // document.getElementById('signature').innerText = data
            if (data.split('|')[0] != 'ycitus'){
                const elementOfflineMessage = document.getElementById('offline-message');
                if (!elementOfflineMessage)  document.getElementById('card').innerHTML += '<li class="offline_message" id="offline-message"><h3>当前已离线</h3></li>';
                const elementToRemove1 = document.getElementById('ip-list');
                const elementToRemove2 = document.getElementById('ip-1');
                const elementToRemove3 = document.getElementById('ip-2');
                const elementToRemove4 = document.getElementById('ip-3');
                const elementToRemove5 = document.getElementById('ip-4');
                const elementToRemove6 = document.getElementById('ip-5');
                const elementToRemove7 = document.getElementById('ip-6');
                if (elementToRemove1) {elementToRemove1.parentNode.removeChild(elementToRemove1);}
                if (elementToRemove2) {elementToRemove2.parentNode.removeChild(elementToRemove2);}
                if (elementToRemove3) {elementToRemove3.parentNode.removeChild(elementToRemove3);}
                if (elementToRemove4) {elementToRemove4.parentNode.removeChild(elementToRemove4);}
                if (elementToRemove5) {elementToRemove5.parentNode.removeChild(elementToRemove5);}
                if (elementToRemove6) {elementToRemove6.parentNode.removeChild(elementToRemove6);}
                if (elementToRemove7) {elementToRemove7.parentNode.removeChild(elementToRemove7);}
            } else {
                const elementToRemove = document.getElementById('offline-message');
                if (elementToRemove) {elementToRemove.parentNode.removeChild(elementToRemove);}
                const elementIpList = document.getElementById('ip-list');
                if (!elementIpList)  document.getElementById('card').innerHTML += '<li class="ip_list" id="ip-list"><h3>当前在线：</h3></li>';
                const ipList = data.split('|')[1].split(',');
                const elementToRemove2 = document.getElementById('ip-1');
                const elementToRemove3 = document.getElementById('ip-2');
                const elementToRemove4 = document.getElementById('ip-3');
                const elementToRemove5 = document.getElementById('ip-4');
                const elementToRemove6 = document.getElementById('ip-5');
                const elementToRemove7 = document.getElementById('ip-6');
                if (elementToRemove2) {elementToRemove2.parentNode.removeChild(elementToRemove2);}
                if (elementToRemove3) {elementToRemove3.parentNode.removeChild(elementToRemove3);}
                if (elementToRemove4) {elementToRemove4.parentNode.removeChild(elementToRemove4);}
                if (elementToRemove5) {elementToRemove5.parentNode.removeChild(elementToRemove5);}
                if (elementToRemove6) {elementToRemove6.parentNode.removeChild(elementToRemove6);}
                if (elementToRemove7) {elementToRemove7.parentNode.removeChild(elementToRemove7);}
                i = 0;
                for (const ip of ipList) {
                    // document.getElementById('signature').innerText = ip;
                    i++;
                    const newLi = document.getElementById('ip-'+i);
                    if(!newLi) {
                        document.getElementById('card').innerHTML += '<li class="ip_show" id="ip-' + i + '"><a onclick="close_ip' + i +
                            '()"><i>' + ip + '</i><span>关闭连接</span></a></li>';
                    }
                }
            }
            add_new_EventListener();
        })
//       .catch(error => console.error('Error fetching client count:', error));
}

function printComplete() {
        document.getElementById('fileTypeMT').innerText = '打印完成，请重新选择'
}

function changeZhuizongmessage() {
    document.getElementById('zhuizongmessage').innerText = '打印完成'
}