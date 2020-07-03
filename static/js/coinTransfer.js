const promise1 = new Promise(function(resolve, reject) {
  resolve('Success!');
  console.log("Success")
});

function sendMoney(money, toAddress, fromAddress, marketID) {
    // Get ERC20 Token contract instance
    var web3 = new Web3(Web3.givenProvider);
    let tokenAddress = "0xab0ed64d89446981b2a07e9789e9520e46a5e01a";
    // let toa = "0x98a91e5645A06345c4e3C1e5724BC109b0A08FE9";
    // let frm = "0x9b1e8f806851F17DB60Dc3E2DD3e30270CFFF8cf";
    // console.log(String(fromAddress));
    // console.log(String(frm));
    let minABI = [
        // transfer
        {
            "constant": false,
            "inputs": [{
                    "name": "_to",
                    "type": "address"
                },
                {
                    "name": "_value",
                    "type": "uint256"
                }
            ],
            "name": "transfer",
            "outputs": [{
                "name": "",
                "type": "bool"
            }],
            "type": "function"
        },
        {
          "constant": true,
          "inputs": [
            {
              "name": "_owner",
              "type": "address"
            }
          ],
          "name": "balanceOf",
          "outputs": [
            {
              "name": "balance",
              "type": "uint256"
            }
          ],
          "payable": false,
          "type": "function"
        }
    ];
    let frm = String(fromAddress);
    let toa = String(toAddress);
    var myContract = new web3.eth.Contract(minABI, tokenAddress, { from: frm });
    myContract.methods.transfer(toa, money).send().then(function(value) {
  console.log(value);
  console.log("Success!")
  $.ajax({
    type : "POST",
    url: "/success/",
    data : {"marketID": marketID},
    success: function(response) {
      location.reload();
       console.log("Done");
     }
  });
}).catch(console.error);
    $('.modal').modal('close');
}


$(document).ready(function() {
    // instantiate by address
    var contractInstance = myContract.address;

    var result = myContract.methods.balanceOf(fromAddress).call().then(function (result) {
        $("#blnce").text(result/1000);
    });



});
