package housework

import (
	"fmt"
	"os"
	"time"
)

/*----- 家事のインターフェース -----*/
type houseWork interface {
	start() string
	end() string
}

/*----- 各種家事の構造体定義 -----*/
/* 洗濯 */
type wash struct {
	name string
	time int
}

func (w wash) start() string {
	return w.name + "を始めます"
}

func (w wash) end() string {
	return w.name +  "が終わりました"
}

/* 掃除 */
type clean struct {
	name string
	room int
	time int
}

func (c clean) start() string {
	return c.name + "を始めます"
}

func (c clean) end() string {
	return c.name + "が終わりました"
}

/* 料理 */
type cook struct {
	name string
	menu string
	time int
}

func (c cook) start() string {
	return c.name + "を始めます"
}

func (c cook) end() string {
	return c.name + "が終わりました"
}

/*----- 関数の定義 -----*/
/* 家事を実行する関数 */
func parallelWork(work interface{}, semaphore chan bool, workControl chan<- bool) {
	/* 実行できるまで待機する */
	semaphore <- true

	switch work := work.(type) {
	case wash:
		/* 作業開始 */
		fmt.Println(work.start())

		/*  実際の作業 */
		for i := work.time; i >= 0; i-- {
			fmt.Println(work.name, "完了までの残り時間:", i)
			time.Sleep(1 * time.Second)
		}

		/* 作業終了 */
		fmt.Println(work.end())
	case clean:
		/* 作業開始 */
		fmt.Println(work.start())

		/*  実際の作業 */
		for j := 1; j <= work.room; j++ {
			fmt.Println(j, "部屋目の掃除開始")
			for i := work.time; i >= 0; i-- {
				fmt.Println(work.name, "完了までの残り時間:", i)
				time.Sleep(1 * time.Second)
			}
		}

		/* 作業終了 */
		fmt.Println(work.end())
	case cook:
		/* 作業開始 */
		fmt.Println(work.start())

		/*  実際の作業 */
		fmt.Println(work.menu, "を作ります")
		for i := work.time; i >= 0; i-- {
			fmt.Println(work.name, "完了までの残り時間:", i)
			time.Sleep(1 * time.Second)
		}

		/* 作業終了 */
		fmt.Println(work.end())
	default:
		fmt.Println("型が違います")
		os.Exit(0)
	}

	/* 処理の終了を通知する */
	<-semaphore

	/* 関数の処理を通知する */
	workControl <- true
}

/* 家事をする関数 */
func Work() {
	/* 変数の定義 */
	/* 平行する数 */
	maxParallelWork := 2

	/* 同一の関数で処理するためインターフェース型に入れる */
	workList := [...]interface{}{
		interface{}(wash{"洗濯", 30}),
		interface{}(clean{"掃除", 2, 10}),
		interface{}(cook{"料理", "オムレツ", 15}),
	}

	/* チャネル */
	workControl := make(chan bool, len(workList))
	semaphore := make(chan bool, maxParallelWork)

	/* ゴルーチンの開始 */
	for _, w := range workList {
		go parallelWork(w, semaphore, workControl)
	}

	/* 処理が完了するまで待機 */
	for i := 0; i < len(workList); i++ {
		<-workControl
	}
}