module levus.gui {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.graphics;
    
    requires org.json;
    requires org.controlsfx.controls;
    requires atlantafx.base;
    //requires com.almasb.fxgl.all;
    requires org.kordamp.ikonli.javafx;
    requires org.kordamp.ikonli.core;
    requires org.kordamp.ikonli.material2;


    requires java.net.http;



    opens levus.gui to javafx.fxml;
    exports levus.gui.chat to javafx.fxml;
    opens levus.gui.chat to javafx.fxml;
    exports levus.gui;
}