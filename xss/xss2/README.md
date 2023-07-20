<h2>Learning point</h2>

<ul>
    <li><h3>HTML5부터 innerHTML의 script태그는 외부 리소스에서 검열된다.</h3></li>
    <li><h3>HTML에는 event와 이를 관리하는 event handler가 있는데, onclick, onload 등으로 script태그를 대신하여 javascript를 동작하게 할 수 있다. </h3></li>
    <li><h3>img태그의 src속성에 옳은 img url을 삽입하여 onload event handler가 동작하게 할 수 있다. 만약 브라우저가 리소스를 display할때 src에 입력된 img url을 불러오는데 실패한다면 onerror event handler가 동작할 수 있다.</h3></li>
</ul>

<h2>How Solved</h2>
<ul>
    <li><h3>xss2문제에서는 vuln.html의 취약점이 돋보인다. 백엔드 코드에서 라우팅된 함수를 살펴보면 단순히 render_template()을 통해 vuln.html파일을 불러온다. vuln.html을 분석해보면 script태그가 작동하지 않을것을 알 수 있으므로 우회방법을 고안해야한다. 백엔드의 check_xss()와 read_url()때문에 사이트를 이용하는 모든 유저는 /vuln 페이지에 접근한다. 따라서 vuln.html의 페이로드를 작성할 때 img태그의 src를 비워두고 onerror event handler를 사용하여 location.href등을 사용하여 쿠키를 탈취하는 javascript코드를 작성하면 문제를 해결할 수 있다
</ul>
