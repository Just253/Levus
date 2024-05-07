module levus.gui {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires com.dlsc.formsfx;
    requires net.synedra.validatorfx;
    requires org.kordamp.bootstrapfx.core;
    //requires com.almasb.fxgl.all;
    


    opens levus.gui to javafx.fxml;
    exports levus.gui;
}