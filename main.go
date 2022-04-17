package main

import (	
	"fmt"
	"net/http"
	"html/template"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
	"strconv"
	"strings"
	"encoding/json"
)

var Db *sqlx.DB
func init() {
    database, err := sqlx.Open("mysql", "**user**:**password**@tcp(127.0.0.1:3306)/**database**")//数据库账号密码
    if err != nil {
        fmt.Println("open mysql failed,", err)
        return
    }
    Db = database
}



func hlwd(w http.ResponseWriter,r *http.Request){
	r.ParseForm()
	begin,er:=r.Form["begin"]
	fmt.Println(begin,er)
	t,_:=template.ParseFiles("html/list.html","html/list-fav.html","html/pagenav.html")

	var bgnum int
	alist:=struct{

		Title string
		
		Paper []struct {
			Title string `db:"title"`
			Tid int `db:"tid"`
			Fav int `db:"fav_count"`
			Uid string `db:"uid"`
			Author string `db:"author"`
			}
		}{}
	if er{	
		bgnum,_=strconv.Atoi(begin[0])
	}else{
		bgnum=0
	}
	alist.Title="Au文库"
	err:=Db.Select(&alist.Paper,"select tid,title,uid,author,fav_count from asoul_paper order by fav_count desc limit ?,50",bgnum*50)
    
	if err != nil {
        fmt.Println("exec failed, ", err)
        return
    }


	t.ExecuteTemplate(w,"dbpage",alist)
}


func jwf(w http.ResponseWriter,r *http.Request){
	r.ParseForm()
	begin,er:=r.Form["begin"]
	fmt.Println(begin,er)
	t,_:=template.ParseFiles("html/list.html","html/list-fav.html","html/pagenavjwf.html")

	var bgnum int
	alist:=struct{

		Title string
		
		Paper []struct {
			Title string `db:"title"`
			Tid int `db:"tid"`
			Fav int `db:"fav_count"`
			Uid string `db:"uid"`
			Author string `db:"author"`
			}
		}{}
	if er{	
		bgnum,_=strconv.Atoi(begin[0])
	}else{
		bgnum=0
	}
	alist.Title="赢组二创文备份"
	err:=Db.Select(&alist.Paper,"select tid,title,uid,author,fav_count from asoul_paper where gid=726457 order by fav_count desc limit ?,100",bgnum*100)    
	if err != nil {
        fmt.Println("exec failed, ", err)
        return
    }
	t.ExecuteTemplate(w,"dbpage",alist)
}
type artinfo struct{
	Title string
	Author string
	Uid string
	Create_time string
}

type comment struct{
	Author string `json:"name"`
	Uid string    `json:"uid"`
	Text template.HTML `json:"text"`
	Create_time string `json:"create_time"`
	Ref_comment struct{
		Author string `json:"name"`
		Uid string `json:"uid"`
		Text template.HTML `json:"text"`
	} `json:"ref_comment"`
	Commentflag bool
}
type article struct{
	Info artinfo
	Mainfloor template.HTML
	Reply [] comment
}



func pp(w http.ResponseWriter,r *http.Request){
	ttid:=strings.Split(r.URL.Path,"/")
	tid:=ttid[len(ttid)-1]
	t,_:=template.ParseFiles("html/fullarticle.html")
	var alltext [] template.HTML

	err:=Db.Select(&alltext,"select textdata from asoul_article where tid=? order by `order`",tid)
	var artlist article

	artlist.Mainfloor=alltext[0]
	
	for index,i := range alltext{
		
		if index==0{
			continue
		}
		var tmp comment
		err = json.Unmarshal([]byte(i), &tmp)
		if err != nil{
			fmt.Println(err)
			return
		}
		if tmp.Ref_comment==struct{
			Author string `json:"name"`
			Uid string `json:"uid"`
			Text template.HTML `json:"text"`
		}{}{
			tmp.Commentflag=false
		}else{
			tmp.Commentflag=true
		}
		artlist.Reply=append(artlist.Reply,tmp)
	}





	if err != nil {
        fmt.Println("exec failed, ", err)
        return
    }
	var att []artinfo

	err=Db.Select(&att,"select title,author,uid,IFNULL(create_time,'未知') as create_time from asoul_paper where tid=?",tid)
	if err != nil {
        fmt.Println("exec failed, ", err)
        return
    }
	
	artlist.Info=att[0]
	if len(artlist.Info.Create_time)>10{
		artlist.Info.Create_time=artlist.Info.Create_time[:19]
	}

	t.ExecuteTemplate(w,"article",artlist)
}

func main(){

server:=http.Server{
	Addr:":80",
}
http.HandleFunc("/",hlwd)
http.HandleFunc("/paper/",pp)
http.HandleFunc("/jwf",jwf)
server.ListenAndServe()

}
