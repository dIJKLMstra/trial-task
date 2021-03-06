/**
 * @author Qi Sun
 * @fileoverview Jobs data analysis
 * @version 3.0
 */

/**
 *  Save our json payload in this dictionary
 *  @global
 */
var jobDict = new Array();

/**
 * Load json payload and find popular skills
 * and list 18 most popular skills on checkboxs we set
 * 
 * @param {json} data Jobs data we crawled
 */
function jobJson(data){     
    jobDict = data;
    /*
        Dic array save each skill's name
        and number of jobs required this skill
        @example 
        [skill1: count_of_skill1, ... ]
    */
    var dic = new Array();
    for(var cur_id in data){
        var skills = data[cur_id].skills;
            for (var skill in skills){
                if(dic[skills[skill]])
                    dic[skills[skill]] += 1;
                else
                    dic[skills[skill]] = 1;
            }
    }

    // sort dic array by value
    var sorted_dic = Object.keys(dic).sort(
        function(a, b){return dic[b] - dic[a];});
    console.log(sorted_dic);

    /*
        write 18 most popular skills' names on checkboxs
        linked with <label id="0/1/2.../17"> </label>
    */
    for(var skill_id = 0; skill_id < 18; skill_id++)
        document.getElementById(skill_id.toString()).innerHTML= 
            sorted_dic[skill_id] + '(' + dic[sorted_dic[skill_id]] + ')';
}

/**
 * Whenever user check a checkbox, 
 * we will match jobs with required skills that user checked
 * and list the jobs in a table showed on downside in website
 */
function jobList(){
    // first we need to clear <div id="jobs_table"> </div> 's text
    table_div = document.getElementById('jobs_table');
    table_div.innerHTML = "";

    // get names of all skills that have been checked 
    // and save them in skills_list
    var skills_list = new Array();
    /*
        first we need to find how many checkboxs have been checked
        linked with <input type="checkbox" name="skill">
    */
    var skills = document.getElementsByName('skill');
    for(var skill_id in skills){
        if(skills[skill_id].checked){
            /*
                get each label's innerHTML
                linked with <label id="0/1/2/.../17"> </label>
            */
            var skill_name = document.
                getElementById(skill_id).innerHTML.split('(')[0];
            skills_list.push(skill_name);
        }
    } 

    // build table now
    var tableObj = document.createElement("table");
    table_div.appendChild(tableObj);
    var tr = document.createElement("tr");
    tableObj.appendChild(tr);
    var th1 = document.createElement("th");
    th1.innerText = "Title";
    tr.appendChild(th1);
    var th2 = document.createElement("th");
    th2.innerText = "Salary";
    tr.appendChild(th2);
    var th3 = document.createElement("th");
    th3.innerText = "Date Posted";
    tr.appendChild(th3);
    var th4 = document.createElement("th");
    th4.innerText = "Date Closed";
    tr.appendChild(th4);

    for(var cur_id in jobDict){
        var skills = jobDict[cur_id].skills;

        // to judge whether this job required all skills in skills_list
        var wantedJob = true;
        for(var skill_name in skills_list){
            if(skills.indexOf(skills_list[skill_name]) == -1){
                wantedJob = false;
                break;
            }
        } 

        // if this job is what we want
        // we add it in this dynamic table 
        if(wantedJob == true){
            var trObj = document.createElement("tr");
            tableObj.appendChild(trObj);
            var td1 = document.createElement("td");
            // job title is link to its original page
            td1.innerHTML = '<a href="' + jobDict[cur_id].job_url + 
                '">' + jobDict[cur_id].job_title + "</a>";
            trObj.appendChild(td1);
            var td2 = document.createElement("td");
            // some jobs didn't mention its salary range
            if(jobDict[cur_id].salary_range.length == 0)
                td2.innerText = 'Not Mentioned';
            else 
                td2.innerText = jobDict[cur_id].salary_range[0] + 
                    ' to ' + jobDict[cur_id].salary_range[1].substring(2);
            trObj.appendChild(td2);
            var td3 = document.createElement("td");
            td3.innerText = jobDict[cur_id].date_posted;
            trObj.appendChild(td3);
            var td4 = document.createElement("td");
            td4.innerText = jobDict[cur_id].date_closed;
            trObj.appendChild(td4);
        }
    }

    /*
        if no job can be found, we will clear the head of table
        linked with <div id="jobs_table"> </div>
    */
    if(skills_list.length == 0 || 
        tableObj.childNodes.length == 1)
        table_div.innerHTML = "";
}