package com.zdiv.jython;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.python.util.PythonInterpreter;

public class JythonRun {
    public static void main(String[] args) throws IOException {
           PythonInterpreter pi = new PythonInterpreter();
           /*
           pi.set("integer", new PyInteger(42));
           pi.exec("square = integer*integer");
           PyInteger square = (PyInteger)pi.get("square");
           System.out.println("square: " + square.asInt());
           */
           if( args.length == 1 ) {
               pi.exec(script);
               pi.exec(fileToString(args[0]));
           } else {
               System.out.println("Usage: ezJavaFx.jar <file>");
           }
    }
    static String fileToString(String fileName) throws IOException {
        return new String(Files.readAllBytes(Paths.get(fileName)), StandardCharsets.UTF_8);
    }
    static String script = "<jython library script>";
}
