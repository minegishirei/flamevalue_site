
var R = 25
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

//var body_element = document.getElementsByTagName("body")[0]
var display_width = window.parent.screen.width
var display_heigth = window.parent.screen.height

var color = d3.scaleOrdinal()
    .range(["#f7d147", "#03a6a6", "#fe736c", "#ec5a31", "#d8345f", "#a7d129", "#f8eeb4", "#fe736c", "#616f39", "#ff6363", "#a7d129", "#d8345f", "#db2ae2"]);

var simulation = d3.forceSimulation()
    .velocityDecay(0.4) //摩擦
    .force('charge', d3.forceManyBody()) //詳細設定は後で
    .force('link', d3.forceLink().id(function (d) {
        return d.name;
    })) //詳細設定は後で
    .force('colllision', d3.forceCollide(40)) //nodeの衝突半径：Nodeの最大値と同じ
    .force('positioningX', d3.forceX()) //詳細設定は後で
    .force('positioningY', d3.forceY()) //詳細設定は後で
    .force('center', d3.forceCenter(width / 2, height / 2)); //重力の中心

//"svg"にZoomイベントを設定
var zoom = d3.zoom()
    .scaleExtent([1 / 4, 4])
    .on('zoom', SVGzoomed);

svg.call(zoom);

//"svg"上に"g"をappendしてdragイベントを設定
var g = svg.append("g")
    .call(d3.drag()
        .on('drag', SVGdragged))


function SVGzoomed() {
    g.attr("transform", d3.event.transform);
}

function SVGdragged(d) {
    d3.select(this).attr('cx', d.x = d3.event.x).attr('cy', d.y = d3.event.y);
};

url = "https://raw.githubusercontent.com/kawadasatoshi/twitter_network/main/{{ acount_name }}"
d3.json(url, function (error, graph) {
    if (error) throw error;


    var link = g.append("g") //svg⇒gに
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke", "#666666") //輪郭線の色指定追加
        .attr("stroke-width", function (d) {
            return Math.sqrt(d.value * 10);
        });

    // nodeの定義
    var node = g.append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(graph.nodes)
        .enter()
        .append('g')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    node.append("svg:image")
        .attr("xlink:href", function (d) { return d.img; })
        .attr("height", R * 2)
        .attr("width", R * 2)
        .attr('clip-path', 'url(#clip)')
        .attr("x", function (d) { return -R; })
        .attr("y", function (d) { return -R; })

    node.on('click', function (d) {
        change_description(d.name)
        change_title(d.name)
    });

    var Defs = svg.append("defs");

    var circles = Defs
        .append('circle')
        .attr('id', 'circle')
        .attr('r', R)
        .attr('cx', 0)
        .attr('cy', 0);

    Defs.append('clipPath')
        .attr('id', 'clip')
        .append('use')
        .attr('xlink:href', '#circle');

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    simulation.force('charge')
        .strength(function (d) {
            return -1000
        }) //node間の力

    simulation.force('positioningX') //X方向の中心に向けた引力
        .strength(0.3)

    simulation.force('positioningY') //Y方向の中心に向けた引力
        .strength(0.3)

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x + display_width / 2;
            })
            .attr("y1", function (d) {
                return d.source.y + display_heigth / 2;
            })
            .attr("x2", function (d) {
                return d.target.x + display_width / 2;
            })
            .attr("y2", function (d) {
                return d.target.y + display_heigth / 2;
            });
        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            })
            .attr('transform', function (d) {
                return 'translate(' + Number(d.x + display_width / 2) + ',' + Number(d.y + display_heigth / 2) + ')'
            }); //nodesの要素が連動して動くように設定
    }
});

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

/**
 * これはいい関数ですよ...
 * おいおいおい
 * 死ぬわあいつ
 * user - ユーザーオブジェクト
 * @param {*} description 
 */
class change_title {

    /**
     * これはいい関数ですよ...
     * おいおいおい
     * 死ぬわあいつ
     * user - ユーザーオブジェクト
     * @param {*} description 
     */
    change_title(params) {
        description_element = document.getElementById("title_id");
        description_element.innerHTML = `
                <a id="twitter_link" target=”_blank”  href="./`+ description + `">`
            + description +
            `network</a>`
    }


    /**
     * これはお試しの関数です。
     * 
     * 実際に作成される。
     * @param {*} description 
     */
    test_function(description){
        document.getElementsById("test").innerHTML = description
    }

}

/**
 * twitterのdescriptionを変更する関数です。
 * 
 * new_titleを引数にとって、description_idを変更します。
 * 
 * **これがむずかしい**
 * 
 * 以下サンプルコード
 * ```js
 * change_description("新しい世界へようこそ")
 * ```
 * 
 * @param {*} new_title 
 */
function change_description(new_title) {
    title_element = document.getElementById("description_id");
    title_element.innerHTML = `
            <a target=”_blank” id="twitter_link" href="https://twitter.com/`+ new_title + `">goto `
        + new_title +
        ` twitter</a>`
}
