extern crate gtk;
extern crate cairo;

use std::cell::RefCell;
use rand::Rng;
use std::f64::consts::PI;
use gtk::prelude::*;
use cairo::ImageSurface;
use cairo::Format;
use cairo::Context;

/* プロットする点の座標 */
struct Point {
    x: f64,
    y: f64,
}

/* プロット結果を描画するためのウィジェットのパラメータ */
struct CanvasStatus {
    width: i32,
    height: i32,
    canvas: gtk::DrawingArea,
    point: Vec<Point>,
    inner: i32,
}

/* CanvasStatusの埋め込み関数 */
impl CanvasStatus {
    /* コンストラクタ */
    pub fn new(width: i32, height:i32) -> Self {
        CanvasStatus{ width: width, height: height, canvas:gtk::DrawingArea::new(), point: Vec::new(), inner: 0 }
    }

    /* 各種データをリセットする */
    pub fn reset_data(&mut self, size: i32)  {
        self.inner = 0;
        self.point.clear();
        Self::generate_point(self, size);
        self.canvas.set_size_request(self.width, self.height);
    }

    /* プロット結果から面積を計算する関数 */
    pub fn calc_area(&self) -> f64 {
        (self.inner as f64 / self.point.len() as f64) * 4.0
    }

    /* 点をプロットする */
    fn draw(&mut self, context: &Context) {
        for i in 0..self.point.len() {
            context.arc(self.point[i].x * self.width as f64, self.height as f64 - self.point[i].y * self.height as f64, 3.0, 0.0, 2.0 * PI);
            if (self.point[i].x * self.point[i].x + self.point[i].y * self.point[i].y) <= 1.0 {
                /* 赤色の点でプロット */
                context.set_source_rgba(1.0, 0.0, 0.0, 1.0); 
                self.inner += 1;
            } else {
                /* 青色の点でプロット*/
                context.set_source_rgba(0.0, 0.0, 1.0, 1.0); 
            }
            context.fill();
        }
    }

    /* 結果をDrawingAreaに描画する */
    fn draw_canvas(&mut self) {
        let image_surface = ImageSurface::create(Format::Rgb24, self.width, self.height).expect("Couldn't create surface");
        let context = Context::new(&image_surface);
    
        context.set_source_rgb(1.0, 1.0, 1.0);
        context.paint();

        context.arc(0.0, self.height as f64, self.height as f64, 3.0 * PI / 2.0, 0.0);
        context.set_source_rgb(0.0, 0.0, 0.0);
        context.stroke();

        Self::draw(self, &context);

        image_surface.flush();

        self.canvas.connect_draw(move |_,context| {
            context.set_source_surface(&image_surface, 0.0, 0.0);
            context.paint();

            Inhibit(false)
        });
    }

    /* ランダムに点を生成する */
    fn generate_point(&mut self, size: i32) {
        for _ in 0..size {
            let random_x = rand::thread_rng().gen_range(0, 100) as f64;
            let random_y = rand::thread_rng().gen_range(0, 100) as f64;
            
            self.point.push(Point{ x: random_x/100.0, y: random_y/100.0 });
        }
    }
}

/* GUIを配置する関数 */
fn generate_gui(window: &gtk::Window, width: i32, height: i32, plots: i32) {
    /* ウィジェットの生成 */
    let vbox = gtk::Box::new(gtk::Orientation::Vertical, 5);

    let label = gtk::Label::new(Some("Monte Carlo method"));
    vbox.pack_start(&label, false, false, 0);

    /* 点を打つウィジェット */
    let mut canvas = CanvasStatus::new(width,height);
    canvas.reset_data(plots);
    canvas.draw_canvas();

    vbox.pack_start(&canvas.canvas, false, false, 0);

    /* 下部のウィジェット */
    /* 内部にプロットされた点を表示する部分 */
    let innerbox = gtk::Box::new(gtk::Orientation::Horizontal, 2);

    let innerlabel = gtk::Label::new(Some("inner : "));
    innerbox.pack_start(&innerlabel, true, true, 0);

    let innerresult = gtk::Label::new(Some(&canvas.inner.to_string()));
    innerbox.pack_start(&innerresult, true, true, 0);

    vbox.pack_start(&innerbox, false, false, 0);

    /* 面積を表示する部分 */
    let areabox = gtk::Box::new(gtk::Orientation::Horizontal, 2);
    
    let arealabel = gtk::Label::new(Some("area : "));
    areabox.pack_start(&arealabel, true, true, 0);

    let arearesult = gtk::Label::new(Some(&canvas.calc_area().to_string()));
    areabox.pack_start(&arearesult, true, true, 0);

    vbox.pack_start(&areabox, false, false, 0);

    /* プロット数を入力する部分 */
    let plotbox = gtk::Box::new(gtk::Orientation::Horizontal, 2);

    let plotlabel = gtk::Label::new(Some("num : "));
    plotbox.pack_start(&plotlabel, true, true, 0);

    let entry = gtk::Entry::new();
    entry.set_text(&plots.to_string());
    plotbox.pack_start(&entry, true, true, 0);

    let button = gtk::Button::with_label("Plot");

    /* ボタンを押されたときのコールバック関数 */
    {
        let canvas_refcall: RefCell<CanvasStatus> = RefCell::new(canvas);
        let wc = window.clone();

        button.connect_clicked(move |_| {
            /* テキストボックスの値を取得する */
            match entry.get_text().parse() {
                Ok(num) => {
                    /* 取得した値をもとに再計算、再描画 */
                    match num {
                        /* 範囲に問題がなければデータをセットし直して再描画する */
                        num if num > 0 => {
                            canvas_refcall.borrow_mut().reset_data(num);
                            canvas_refcall.borrow_mut().draw_canvas();

                            /* 表示結果の更新 */
                            arearesult.set_text(&canvas_refcall.borrow_mut().calc_area().to_string());
                            innerresult.set_text(&canvas_refcall.borrow_mut().inner.to_string());
                        },
                        /* 範囲に問題があればダイアログを表示する */
                        _ => {
                            let dialog = gtk::MessageDialog::new(
                                Some(&wc),
                                gtk::DialogFlags::MODAL,
                                gtk::MessageType::Error,
                                gtk::ButtonsType::Close,
                                &("Invalid value.")
                            );
                            dialog.run();
                            unsafe {
                                dialog.destroy();
                            }
                        },
                    }
                },
                /* 取得したテキストが数値に変換できないときはダイアログを表示する */
                Err(err) => {
                    let dialog = gtk::MessageDialog::new(
                        Some(&wc),
                        gtk::DialogFlags::MODAL,
                        gtk::MessageType::Error,
                        gtk::ButtonsType::Close,
                        &err.to_string()
                    );
                    dialog.run();
                    unsafe {
                        dialog.destroy();
                    }
                },
            };
        });
    }

    plotbox.pack_start(&button, true, true, 0);

    vbox.pack_start(&plotbox, true, true, 0);
    window.add(&vbox);

    /* プログラムを終了するイベント */
    window.connect_delete_event(|_, _| {
        gtk::main_quit();
        Inhibit(false)
    });

    /* 画面を描画する */
    window.show_all();
}

fn main() {
    /* GTKの初期化 */
    gtk::init().expect("Failed to initialize GTK.");

    /* ウィンドウインスタンスの生成 */
    let window = gtk::Window::new(gtk::WindowType::Toplevel);
    window.set_title("Monte Carlo method");
    window.set_default_size(400, 500);
    
    /* GUIを生成 */
    generate_gui(&window, 400, 400, 3000);

    gtk::main();
}
