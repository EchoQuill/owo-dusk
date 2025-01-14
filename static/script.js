/*
This file is part of owo-dusk.

Copyright (c) 2024-present EchoQuill

Portions of this file are based on code by EchoQuill, licensed under the
GNU General Public License v3.0 (GPL-3.0).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Website originally created by TheNabbu (https://github.com/TheNabbu)
for the project Slashy (https://github.com/TahaGorme/slashy), licensed
under the MIT License. For details, see:
https://github.com/TahaGorme/slashy/blob/main/LICENSE

This file has been modified for OwO-Dusk, under permission and in
compliance with the MIT License.

Modified version licensed under GPL-3.0.
*/


/*
var password =
    localStorage.getItem("password") || prompt("Enter Password");
if (password) localStorage.setItem("password", password);
*/


/* Please try to understand that I am not good with javascript,
so expect some funny codes here. I'll appriciate it if you can letme know 
how I can further improve this code! */


/* fix min max check for defqault cds
 */

var autoLootboxC = document.getElementById("cb1");
var autoCrateC = document.getElementById("cb2");
var useSlashCommandsC = document.getElementById("cb3");
var offlineStatusC = document.getElementById("cb4");
var webhookC = document.getElementById("cb5");
var autoGemC = document.getElementById("cb6");

// Main
var huntC = document.getElementById("cb7");
var battleC = document.getElementById("cb8");
var owoC = document.getElementById("cb9");
var lvlGrindC = document.getElementById("cb10");
var prayC = document.getElementById("cb11");
var curseC = document.getElementById("cb12");
var cookieC = document.getElementById("cb13");
var autoDailyC = document.getElementById("cb14");
var lotteryC = document.getElementById("cb15");
var giveawayJoinerC = document.getElementById("cb16");

// Gamble 
var coinflipC = document.getElementById("cb17");
var slotsC = document.getElementById("cb18");

// Cooldowns
var longCooldownMinC = document.getElementById("b1");
var longCooldownMaxC = document.getElementById("b2");
var moderateCooldownMinC = document.getElementById("b3");
var moderateCooldownMaxC = document.getElementById("b4");
var shortCooldownMinC = document.getElementById("b5");
var shortCooldownMaxC = document.getElementById("b6");
var briefCooldownMinC = document.getElementById("b7");
var briefCooldownMaxC = document.getElementById("b8");
var captchaRestartMinC = document.getElementById("b9");
var captchaRestartMaxC = document.getElementById("b10");

// Initialize these outside func to make it global
var webhook = {};
var gems = {};
var hunt = {};
var battle = {};
var owo = {};
var lvlGrind = {};
var pray = {};
var curse = {};
var cookie = {};
var lottery = {};
var giveawayJoiner = {};
var coinflip = {};
var slots = {};

// Save and send as JSON

const save_data = (json_data) => {
    fetch("/api/saveThings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            password: "test",
        },
        body: JSON.stringify(json_data),
    }).then((response) => {
        console.log("Response received:", response);
        return response.json();
    }).then((data) => {
        console.log("Response data:", data);
    }).catch((error) => {
        console.log("Error occurred:", error);
    });
}

// load config

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded, attempting to fetch configuration...");
    fetch("/api/config", {
        headers: { password: "password" },
    })
        .then((res) => {
            if (!res.ok) {
                throw new Error(`Failed to load config: ${res.status}`);
            }
            return res.json();
        })
        .then((config) => {
            console.log("Configuration loaded:", config);

            // Misc
            autoLootboxC.checked = config.autoUse?.autoLootbox || false;
            autoCrateC.checked = config.autoUse?.autoCrate || false;
            useSlashCommandsC.checked = config?.useSlashCommands|| false;
            offlineStatusC.checked = config?.offlineStatus|| false;
            webhookC.checked = config.webhook?.enabled || false;
            autoGemC.checked = config.autoUse.gems?.enabled || false;


            // Main (MISSING PRAY!)
            huntC.checked = config.commands.hunt?.enabled || false;
            battleC.checked = config.commands.battle?.enabled || false;
            owoC.checked = config.commands.owo?.enabled || false;
            lvlGrindC.checked = config.commands.lvlGrind?.enabled || false;
            cookieC.checked = config.commands.cookie?.enabled || false;
            lotteryC.checked = config.commands.lottery?.enabled || false;

            autoDailyC.checked = config?.autoDaily || false;
            giveawayJoinerC.checked = config.giveawayJoiner?.enabled || false;

            // Cooldowns
            longCooldownMinC.innerText = config.defaultCooldowns.longCooldown[0];
            longCooldownMaxC.innerText = config.defaultCooldowns.longCooldown[1];
            moderateCooldownMinC.innerText = config.defaultCooldowns.moderateCooldown[0];
            moderateCooldownMaxC.innerText = config.defaultCooldowns.moderateCooldown[1];
            shortCooldownMinC.innerText = config.defaultCooldowns.shortCooldown[0];
            shortCooldownMaxC.innerText = config.defaultCooldowns.shortCooldown[1];
            briefCooldownMinC.innerText = config.defaultCooldowns.briefCooldown[0];
            briefCooldownMaxC.innerText = config.defaultCooldowns.briefCooldown[1];
            captchaRestartMinC.innerText = config.defaultCooldowns.captchaRestart[0];
            captchaRestartMaxC.innerText = config.defaultCooldowns.captchaRestart[1];

            //  Gamble
            coinflipC.checked = config.gamble.coinflip?.enabled || false;
            slotsC.checked = config.gamble.slots?.enabled || false;


            /*Rest (Settings)*/

            // set1 - Webhooks

            webhook = {
                "webhookUselessLog": config.webhook.webhookUselessLog,
                "webhookUrl": config.webhook.webhookUrl,
                "webhookUserIdToPingOnCaptcha": config.webhook.webhookUserIdToPingOnCaptcha,
            };

            // set2 - Gems
            gems = {};

            // set3 - hunt
            hunt = {
                "enabled": config.commands.hunt.enabled,
                "cooldown": config.commands.hunt.cooldown,
                "useShortForm": config.commands.hunt.useShortForm,
            };

            // set4 - battle
            battle = {
                "enabled": config.commands.battle.enabled,
                "cooldown": config.commands.battle.cooldown,
                "useShortForm": config.commands.battle.useShortForm,
            };

            // set5 - owo
            owo = {
                "cooldown": config.commands.owo.cooldown,
            };

            // set6 - level grind
            lvlGrind = {
                "cooldown": config.commands.lvlGrind.cooldown,
                "useQuoteInstead": config.commands.lvlGrind.useQuoteInstead,
                "minLengthForRandomString": config.commands.lvlGrind.minLengthForRandomString,
                "maxLengthForRandomString": config.commands.lvlGrind.maxLengthForRandomString,

            };

            // set7 - pray
            pray = {
                "cooldown": config.commands.pray.cooldown,
                "pingUser": config.commands.pray.pingUser,
            };

            // set8 - curse
            curse = {
                "cooldown": config.commands.curse.cooldown,
                "pingUser": config.commands.curse.pingUser,
            };

            // set9 - cookie
            cookie = {
                "userid": config.commands.cookie.userid,
                "pingUser": config.commands.cookie.pingUser,
            };

            // set10 - lottery
            lottery = {
                "amount": config.commands.lottery.amount,
            };

            // set11 - giveaway
            giveawayJoiner = {
                "cooldown": config.giveawayJoiner.cooldown,
            };

            // set12 - cf
            coinflip = {
                "startValue": config.gamble.coinflip.startValue,
                "multiplierOnLose": config.gamble.coinflip.multiplierOnLose,
                "cooldown": config.gamble.coinflip.cooldown,
            };

            // set13 - slots
            slots = {
                "startValue": config.gamble.slots.startValue,
                "multiplierOnLose": config.gamble.slots.multiplierOnLose,
                "cooldown": config.gamble.slots.cooldown,
            };


        })
        .catch((error) => {
            console.error("Error fetching configuration:", error);
            alert("Failed to load configuration. Please check the console for details.");
        });
});



var save = document.getElementById("save");
var credits = document.getElementById("credits")

document.addEventListener("DOMContentLoaded", () => {
    // Select elements by class "ct"
    var cooldownsEl = document.querySelectorAll(".ct");

    // Add click event listeners to each element
    cooldownsEl.forEach((element) => {
        console.log("Adding listener to: ", element);  // Check if elements are found
        element.addEventListener("click", () => {
            var input = prompt(`Enter new value for ${element.innerText}`);
            if (input && !isNaN(input)) {
                element.innerText = input;
            } else {
                alert("Please enter a valid number.");
            }
        }); 
    });
    credits.addEventListener("click", () => {
        alert("Website made by TheNabbu, Modified by Echoquill");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    /*
    set1 = webhook
    set2 = gems
    set3 = hunt
    set4 = battle
    set5 = owo
    set6 = level grind
    set7 = pray//curse
    set8 = cookie
    set9 = daily
    set10 = lottery
    set11 = giveaway
    */
    
    var cooldownsEl = document.querySelectorAll(".cda");

    cooldownsEl.forEach((element) => {
        console.log("Adding listener to: ", element);  // Check if elements are found
        element.addEventListener("click", () => {
            var elementName = element.id.trim().toLowerCase();
            var inputContent = "";

            if (elementName === 'set1') {
                inputContent = `
                    <label for="inp1">Enter Webhook URL:</label>
                    <input type="url" id="inp1" placeholder="https://discord.com/api/...." value="">
                    <label for="inp2">Enable Webhook Useless Log:</label>
                    <input type="checkbox" id="inp2">
                    <label for="inp3">Enter user id of user to ping</label>
                    <input type="number" id="inp3" placeholder="leave as is for none">
                    `;
                
            } else if (elementName === 'set2') {
                inputContent = `
                    <label for="inp4">Enter number of gems:</label>
                    <input type="number" id="inp4" placeholder="Enter a valid number">
                    `;
            } else if (elementName === 'set3') {
                inputContent = `
                    <label for="inp5">Minimum Cooldown:</label>
                    <input type="number" id="inp5" placeholder="Enter a valid number(seconds)">
                    <label for="inp6">Maximum Cooldown:</label>
                    <input type="number" id="inp6" placeholder="Enter a valid number(seconds)">
                    <label for="inp7">Use shortform:</label>
                    <input type="checkbox" id="inp7">
                    `;
            } else if (elementName === 'set4') {
                inputContent = `
                    <label for="inp8">Minimum Cooldown:</label>
                    <input type="number" id="inp8" placeholder="Enter a valid number(seconds)">
                    <label for="inp9">Maximum Cooldown:</label>
                    <input type="number" id="inp9" placeholder="Enter a valid number(seconds)">
                    <label for="inp10">Use shortform:</label>
                    <input type="checkbox" id="inp10">
                    `;
            } else if (elementName === 'set5') {
                inputContent = `
                    <label for="inp11">Minimum Cooldown:</label>
                    <input type="number" id="inp11" placeholder="Enter a valid number(seconds)">
                    <label for="inp12">Maximum Cooldown:</label>
                    <input type="number" id="inp12" placeholder="Enter a valid number(seconds)">
                    `;
            } else if (elementName === 'set6') {
                inputContent = `
                    <label for="inp13">Minimum Cooldown:</label>
                    <input type="number" id="inp13" placeholder="Enter a valid number(seconds)">
                    <label for="inp14">Maximum Cooldown:</label>
                    <input type="number" id="inp14" placeholder="Enter a valid number(seconds)">
                    <label for="inp15">Minimum Text Size:</label>
                    <input type="number" id="inp15" placeholder="Enter a valid number">
                    <label for="inp16">Maximum Text Size:</label>
                    <input type="number" id="inp16" placeholder="Enter a valid number">
                    <label for="inp17">Use quotes instead of random string:</label>
                    <input type="checkbox" id="inp17">
                    `;
            } else if (elementName === 'set7') {
                inputContent = `
                    <label for="inp18">Minimum Cooldown:</label>
                    <input type="number" id="inp18" placeholder="Enter a valid number(seconds)">
                    <label for="inp19">Maximum Cooldown:</label>
                    <input type="number" id="inp19" placeholder="Enter a valid number(seconds)">
                    <label for="inp20">Ping user:</label>
                    <input type="checkbox" id="inp20">
                    `;
            } else if (elementName === 'set8') {
                inputContent = `
                    <label for="inp21">Minimum Cooldown:</label>
                    <input type="number" id="inp21" placeholder="Enter a valid number(seconds)">
                    <label for="inp22">Maximum Cooldown:</label>
                    <input type="number" id="inp22" placeholder="Enter a valid number(seconds)">
                    <label for="inp23">Ping user:</label>
                    <input type="checkbox" id="inp23">
                    `;
            } else if (elementName === 'set9') {
                inputContent = `
                    <label for="inp24">User to give cookie:</label>
                    <input type="text" id="inp24" placeholder="Leave it as 0 if none." pattern="\\d*">
                    <label for="inp25">Ping user while sending command:</label>
                    <input type="checkbox" id="inp25">
                    `;
            } else if (elementName === 'set10') {
                inputContent = `
                    <label for="inp26">Cash to spend:</label>
                    <input type="number" id="inp26" placeholder="Enter a valid number">
                    `;
            } else if (elementName === 'set11') {
                inputContent = `
                    <label for="inp27">Minimum Cooldown:</label>
                    <input type="number" id="inp27" placeholder="Enter a valid number(seconds)">
                    <label for="inp28">Maximum Cooldown:</label>
                    <input type="number" id="inp28" placeholder="Enter a valid number(seconds)">
                    `;
            } else if (elementName == 'set12') {
                inputContent = `
                    <label for="inp29">Minimum Cooldown:</label>
                    <input type="number" id="inp29" placeholder="Enter a valid number(seconds)">
                    <label for="inp30">Maximum Cooldown:</label>
                    <input type="number" id="inp30" placeholder="Enter a valid number(seconds)">
                    <label for="inp31">Start Value:</label>
                    <input type="number" id="inp31" placeholder="Enter a valid number">
                    <label for="inp32">Multiplier on lose:</label>
                    <input type="number" id="inp32" placeholder="Enter a valid number">
                    `;
            } else if (elementName == 'set13') {
                inputContent = `
                    <label for="inp33">Minimum Cooldown:</label>
                    <input type="number" id="inp33" placeholder="Enter a valid number(seconds)">
                    <label for="inp34">Maximum Cooldown:</label>
                    <input type="number" id="inp34" placeholder="Enter a valid number(seconds)">
                    <label for="inp35">Start Value:</label>
                    <input type="number" id="inp35" placeholder="Enter a valid number">
                    <label for="inp36">Multiplier on lose:</label>
                    <input type="number" id="inp36" placeholder="Enter a valid number">
                    `;
            } else if (elementName == 'set14') {
                /*
                BLACKJACK!
                */
                inputContent = `
                    <label for="inp37">Minimum Cooldown:</label>
                    <input type="number" id="inp37" placeholder="Enter a valid number(seconds)">
                    <label for="inp38">Maximum Cooldown:</label>
                    <input type="number" id="inp38" placeholder="Enter a valid number(seconds)">
                    `;
            } else {
                inputContent = "<p>Invalid Element</p>";
            }

            // Create the modal content dynamically
            const modal = document.createElement("div");
            modal.classList.add("popup-modal");
            modal.innerHTML = `
                <div class="popup-content">
                    <h3>Configure ${element.innerText}</h3>
                    ${inputContent}
                    <button id="saveInput">Save</button>
                    <button id="cancelInput">Cancel</button>
                </div>
            `;
            document.body.appendChild(modal);

            // Ensure the values are set properly, and provide default values if undefined
            const setValues = (inputId, value) => {
                const element = document.getElementById(inputId);
                if (element) {
                    if (typeof value === 'boolean') {
                        element.checked = value;
                    } else {
                        element.value = value || ''; // Default to empty string if value is undefined
                    }
                }
            };

            // Webhook (set1)
            setValues("inp1", webhook?.webhookUrl);
            setValues("inp2", webhook?.webhookUselessLog);
            setValues("inp3", webhook?.webhookUserIdToPingOnCaptcha);

            // Gems (set2) - Skipped as per original code

            // Hunt (set3)
            setValues("inp5", hunt?.cooldown?.[0]);
            setValues("inp6", hunt?.cooldown?.[1]);
            setValues("inp7", hunt?.useShortForm);

            // Battle (set4)
            setValues("inp8", battle?.cooldown?.[0]);
            setValues("inp9", battle?.cooldown?.[1]);
            setValues("inp10", battle?.useShortForm);

            // Owo (set5)
            setValues("inp11", owo?.minCooldown);
            setValues("inp12", owo?.maxCooldown);

            // Level Grind (set6)
            setValues("inp13", lvlGrind?.cooldown?.[0]);
            setValues("inp14", lvlGrind?.cooldown?.[1]);
            setValues("inp15", lvlGrind?.minLengthForRandomString);
            setValues("inp16", lvlGrind?.maxLengthForRandomString);
            setValues("inp17", lvlGrind?.useQuoteInstead);

            // Pray (set7)
            setValues("inp18", pray?.cooldown?.[0]);
            setValues("inp19", pray?.cooldown?.[1]);
            setValues("inp20", pray?.pingUser);

            // Curse (set8)
            setValues("inp21", curse?.cooldown?.[0]);
            setValues("inp22", curse?.cooldown?.[1]);
            setValues("inp23", curse?.pingUser);

            // Cookie (set9)
            setValues("inp24", cookie?.userid);
            setValues("inp25", cookie?.pingUser);

            // Lottery (set10)
            setValues("inp26", lottery?.amount);

            // Giveaway (set11)
            setValues("inp27", giveawayJoiner?.cooldown?.[0]);
            setValues("inp28", giveawayJoiner?.cooldown?.[1]);

            // coinflip (set12)
            setValues("inp29", coinflip?.cooldown?.[0]);
            setValues("inp30", coinflip?.cooldown?.[1]);
            setValues("inp31", coinflip?.startValue);
            setValues("inp32", coinflip?.multiplierOnLose);
            //slots (set12)
            setValues("inp33", slots?.cooldown?.[0]);
            setValues("inp34", slots?.cooldown?.[1]);
            setValues("inp35", slots?.startValue);
            setValues("inp36", slots?.multiplierOnLose);
            

            const convert_float = (min, max) => {
                // why doesn't js have a way to send two data without arrays ;(
                return [parseFloat(min), parseFloat(max)];
            };

            const validate_float = (min, max) => {
                if (!isNaN(min) && !isNaN(max)) {
                    if ((min < max) && min >=0 && max >= 0) {
                        return true;
                    }
                }
                return false;
            }

            const validate_int = (int1, int2) => {
                return !isNaN(int1) && !isNaN(int2) && int1 >= 0 && int2 >= 0;
            };


            // Save and cancel event listeners
            document.getElementById("saveInput").addEventListener("click", () => {
                // Save the values when clicked
                if (elementName === 'set1') {  // webhook
                    webhook.webhookUrl = document.getElementById("inp1").value;
                    webhook.webhookUselessLog = document.getElementById("inp2").checked;
                    webhook.webhookUserIdToPingOnCaptcha = document.getElementById("inp3").value;

                    save_data({webhook});
            
                    console.log("Webhook Settings Saved:");
                    console.log("Webhook URL:", webhook.webhookUrl);
                    console.log("Webhook Useless Log Enabled:", webhook.webhookUselessLog);
                    console.log("User ID to Ping:", webhook.webhookUserIdToPingOnCaptcha);
                } 
                else if (elementName === 'set2') {  // gems
                    // area for gems, inp4
                } 
                else if (elementName === 'set3') {  // hunt

                    const minCooldown = parseFloat(document.getElementById("inp5").value);
                    const maxCooldown = parseFloat(document.getElementById("inp6").value);

                    if (validate_float(minCooldown, maxCooldown)) {
                        hunt.cooldown[0] = minCooldown;
                        hunt.cooldown[1] = maxCooldown;
                        hunt.useShortForm = document.getElementById("inp7").checked;

                        save_data({commands: { hunt }})

                        console.log("Hunt Settings Saved:");
                        console.log("Minimum Cooldown:", hunt.cooldown[0]);
                        console.log("Maximum Cooldown:", hunt.cooldown[1]);
                        console.log("Use Shortform:", hunt.useShortForm);

                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                    }
                } 
                else if (elementName === 'set4') {  // battle
                    const minCooldown = parseFloat(document.getElementById("inp8").value);
                    const maxCooldown = parseFloat(document.getElementById("inp9").value);

                    if (validate_float(minCooldown, maxCooldown)) {
                        battle.cooldown[0] = minCooldown;
                        battle.cooldown[1] = maxCooldown;
                        battle.useShortForm = document.getElementById("inp10").checked;

                        save_data({commands: { battle }})

                        console.log("battle Settings Saved:");
                        console.log("Minimum Cooldown:", battle.cooldown[0]);
                        console.log("Maximum Cooldown:", battle.cooldown[1]);
                        console.log("Use Shortform:", battle.useShortForm);

                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                    }
                } 
                else if (elementName === 'set5') {  // owo

                    const minCooldown = parseFloat(document.getElementById("inp11").value);
                    const maxCooldown = parseFloat(document.getElementById("inp12").value);

                    if (validate_float(minCooldown, maxCooldown)) {
                        owo.cooldown = [minCooldown, maxCooldown];

                        save_data({commands: { owo }})

                        console.log("OwO Settings Saved:");
                        console.log("Cooldown Range:", owo.cooldown);
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                    }
                }
                else if (elementName === 'set6') {  // level grind

                    const minCooldown = parseFloat(document.getElementById("inp13").value);
                    const maxCooldown = parseFloat(document.getElementById("inp14").value);
                    const minLengthForRandomString = parseInt(document.getElementById("inp15").value);
                    const maxLengthForRandomString = parseInt(document.getElementById("inp16").value);

                    if (validate_int(minLengthForRandomString, maxLengthForRandomString)) {
                        if (minLengthForRandomString < maxLengthForRandomString) {
                            lvlGrind.minLengthForRandomString = minLengthForRandomString;
                            lvlGrind.maxLengthForRandomString = maxLengthForRandomString;
                        } else {
                            alert("minLengthForRandomString must be smaller than maxLengthForRandomString");
                            return;
                        }
                    } else {
                        alert("Invalid integer values for minLengthForRandomString or maxLengthForRandomString");
                        return;
                    }
                    if (validate_float(minCooldown, maxCooldown)) {
                        lvlGrind.cooldown[0] = minCooldown;  // min cd
                        lvlGrind.cooldown[1] = maxCooldown;  // max cd
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                        return;
                    }
                    lvlGrind.useQuoteInstead = document.getElementById("inp17").checked;  // use quotes
                    save_data({commands: { lvlGrind }});
            
                    console.log("Level Grind Settings Saved:");
                    console.log("Minimum Cooldown:", lvlGrind.cooldown[0]);
                    console.log("Maximum Cooldown:", lvlGrind.cooldown[1]);
                    console.log("Minimum Length for Random String:", lvlGrind.minLengthForRandomString);
                    console.log("Maximum Length for Random String:", lvlGrind.maxLengthForRandomString);
                    console.log("Use Quotes:", lvlGrind.useQuoteInstead);
                } 
                else if (elementName === 'set7') {  // pray
                    const minCooldown = parseFloat(document.getElementById("inp18").value);
                    const maxCooldown = parseFloat(document.getElementById("inp19").value);
                    if (validate_float(minCooldown, maxCooldown)) {
                        pray.cooldown[0] = minCooldown;  // min cd
                        pray.cooldown[1] = maxCooldown;  // max cd
                        pray.pingUser = document.getElementById("inp20").checked;  // ping user   
                        save_data({commands: { pray }});
                        
                        console.log("Pray Settings Saved:");
                        console.log("Minimum Cooldown:", pray.cooldown[0]);
                        console.log("Maximum Cooldown:", pray.cooldown[1]);
                        console.log("Ping User:", pray.pingUser);
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                    }
                } 
                else if (elementName === 'set8') {  // curse
                    const minCooldown = parseFloat(document.getElementById("inp21").value);
                    const maxCooldown = parseFloat(document.getElementById("inp22").value);
                    if (validate_float(minCooldown, maxCooldown)) {
                        curse.cooldown[0] = minCooldown;  // min cd
                        curse.cooldown[1] = maxCooldown;  // max cd
                        curse.pingUser = document.getElementById("inp23").checked;  // ping user    
                        save_data({commands: { curse }});
                        
                        console.log("Curse Settings Saved:");
                        console.log("Minimum Cooldown:", curse.cooldown[0]);
                        console.log("Maximum Cooldown:", curse.cooldown[1]);
                        console.log("Ping User:", curse.pingUser);
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                    }
                } 
                else if (elementName === 'set9') {  // cookie
                    const userid = parseInt(document.getElementById("inp24").value);
                    if (!isNaN(userid)) {
                        if (userid==0) {
                            cookie.userid = null;
                        } else {
                            cookie.userid = userid;
                        }
                        cookie.pingUser = document.getElementById("inp25").checked;
                        save_data({commands: { cookie }});
                        console.log("Cookie Settings Saved:");
                        console.log("User ID:", cookie.userid);
                        console.log("Ping User:", cookie.pingUser);
                    } else {
                        alert("Invalid integer values for userid");
                    }
                }
                else if (elementName === 'set10') {  // lottery
                    const amount = parseInt(document.getElementById("inp26").value);
                    if (!isNaN(amount)) {
                        lottery.amount = amount
                        save_data({commands: { lottery }});
                        console.log("Lottery Settings Saved:");
                        console.log("Amount:", lottery.amount);
                    } else {
                        alert("Invalid integer values for amount");
                    }                  
                } 
                else if (elementName === 'set11') {  // giveaway
                    const minCooldown = parseFloat(document.getElementById("inp27").value);
                    const maxCooldown = parseFloat(document.getElementById("inp28").value);

                    if (validate_float(minCooldown, maxCooldown)) {
                        giveawayJoiner.cooldown = [minCooldown, maxCooldown];
                        save_data(giveawayJoiner);
                        console.log("Giveaway Settings Saved:");
                        console.log("Minimum Cooldown:", giveawayJoiner.cooldown[0]);
                        console.log("Maximum Cooldown:", giveawayJoiner.cooldown[1]);
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                    }
                }                else if (elementName === 'set12') {  // cf
                    const minCooldown = parseFloat(document.getElementById("inp29").value);
                    const maxCooldown = parseFloat(document.getElementById("inp30").value);
                    const startValue = parseInt(document.getElementById("inp31").value);
                    const multiplierOnLose = parseFloat(document.getElementById("inp32").value);

                    if (validate_float(minCooldown, maxCooldown)) {
                        coinflip.cooldown = [minCooldown, maxCooldown];
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                        return;
                    }
                    if (validate_int(startValue, multiplierOnLose)) {
                        coinflip.startValue = startValue;
                        coinflip.multiplierOnLose = multiplierOnLose;
                        save_data({gamble: {coinflip} });

                    }
                }
                else if (elementName === 'set13') {  // slots
                    const minCooldown = parseFloat(document.getElementById("inp33").value);
                    const maxCooldown = parseFloat(document.getElementById("inp34").value);
                    const startValue = parseInt(document.getElementById("inp35").value);
                    const multiplierOnLose = parseFloat(document.getElementById("inp36").value);

                    if (validate_float(minCooldown, maxCooldown)) {
                        slots.cooldown = [minCooldown, maxCooldown];
                    } else {
                        alert("Invalid cooldown values. Please ensure they are numbers and min < max.");
                        return;
                    }
                    if (validate_int(startValue, multiplierOnLose)) {
                        slots.startValue = startValue;
                        slots.multiplierOnLose = multiplierOnLose;
                        save_data({gamble: {slots} });

                    }
                }
                // Show confirmation and remove modal
                //alert(`Settings for ${elementName} saved!`);
                modal.remove();  // Remove modal after saving
            });
            

            document.getElementById("cancelInput").addEventListener("click", () => {
                modal.remove();  // Remove modal without saving
            });
        });
    });
});




document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded");

    var save = document.getElementById("save");

    if (save) {
        console.log("Save button found");
        save.addEventListener("click", () => {
            console.log("Received request");
            save_data({
                    
                useSlashCommands: useSlashCommandsC.checked,
                offlineStatus: offlineStatusC.checked,
                webhook: {enabled: webhookC.checked,},
                autoUse: {
                    autoLootbox: autoLootboxC.checked,
                    autoCrate: autoCrateC.checked,
                    gems: {enabled: autoGemC.checked},
                },
                commands: {
                    hunt: {enabled: huntC.checked,},
                    battle: {enabled: battleC.checked,},
                    owo: {enabled: owoC.checked,},
                    lvlGrind: {enabled: lvlGrindC.checked,},
                    pray: {enabled: prayC.checked,},
                    curse: {enabled: curse.Cchecked,},
                    cookie: {enabled: cookieC.checked,},
                    lottery: {enabled: lotteryC.checked,},
                },
                gamble: {
                    coinflip: {enabled: coinflipC.checked,},
                    slots: {enabled: slotsC.checked,},
                },
                autoDaily: autoDailyC.checked,
                giveawayJoiner: {enabled: giveawayJoinerC.checked,},

                defaultCooldowns: {
                    longCooldown: [Number(longCooldownMinC.innerText), Number(longCooldownMaxC.innerText)],
                    moderateCooldown: [Number(moderateCooldownMinC.innerText), Number(moderateCooldownMaxC.innerText)],
                    shortCooldown: [Number(shortCooldownMinC.innerText), Number(shortCooldownMaxC.innerText)],
                    briefCooldown: [Number(briefCooldownMinC.innerText), Number(briefCooldownMaxC.innerText)],
                    captchaRestart: [Number(captchaRestartMinC.innerText), Number(captchaRestartMaxC.innerText)],
                },
            })
        });
    } else {
        console.log("Save button not found");
    }
    var reset = document.querySelector(".re");
    reset.addEventListener("click", () => {
        window.location.reload();
    });

    // Test
    var logContainer = document.getElementById("logContainer");

    function addLog(log) {
        const logItem = document.createElement("li");
        logItem.innerText = log;
        logContainer.appendChild(logItem);
        logContainer.scrollTop = logContainer.scrollHeight;  // Scroll to bottom
    }
    //addLog("test");
    // Initial log fetch
    fetch("/api/console")
        .then((response) => response.text())
        .then((logs) => {
            logContainer.innerHTML = logs;  // Display logs in container
            logContainer.scrollTop = logContainer.scrollHeight;  // Scroll to bottom
        })
        .catch((error) => console.error("Error fetching logs:", error));
    
    // Update logs every 130ms
    setInterval(() => {
        fetch("/api/console")
            .then((response) => response.text())
            .then((logs) => {
                logContainer.innerHTML = logs;
                logContainer.scrollTop = logContainer.scrollHeight;
            })
            .catch((error) => console.error("Error fetching logs:", error));
    }, 500);

});
//

