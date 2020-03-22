package com.boraji.tutorial.springboot.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController

public class HelloController {

    String str = null;
    String str1 = null;
    String str2 = null;

//////Code to get validated data from user interface///////////////////////
    @RequestMapping("/")
    @CrossOrigin
    public String meth(@RequestParam("Source_URL") final String name, @RequestParam("tok_lin") final String name1,
                    @RequestParam("count") final String name2) throws IOException {

        str = name;
        str1 = name1;
        str2 = name2;
        final String rname = "Output.py";
        final String command5 = "ren " + str + " " + rname;
        final ProcessBuilder builder6 = new ProcessBuilder("cmd.exe", "/c",
                        "cd \"C:\\Users\\320074769\\Downloads\" && " + command5);
        final Process p5 = builder6.start();
        try {
            p5.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }

        final String command4 = "python " + rname;
        final ProcessBuilder builder5 = new ProcessBuilder("cmd.exe", "/c",
                        "cd \"C:\\Users\\320074769\\Downloads\" && " + command4);

        final Process p4 = builder5.start();
        try {
            p4.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
        return "\"Got your report :)\"";

    }

    @RequestMapping("/Final")
    public String index1() {
        return "Final";
    }

/////////////Code to run JSCPD tool and generate report////////////////
    @RequestMapping("/test")
    public String index2() throws IOException {
        //// Process to clone the code/////
        final String cmd1 = "git clone " + str;
        final ProcessBuilder builder1 = new ProcessBuilder("cmd.exe", "/c", "cd \"C:\\test\" && " + cmd1);
        final Process p = builder1.start();
        try {
            p.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
///Process to run JSCPD tool//////
        String fileName = str.substring(str.lastIndexOf('/') + 1);
        fileName = fileName.substring(0, fileName.length() - 4);

        final String cmd2 = "jscpd --min-" + str1 + " " + str2
                        + " --reporters html --output C:\\test --mode strict C:\\test\\" + fileName;

        final ProcessBuilder builder2 = new ProcessBuilder("cmd.exe", "/c", "cd \"C:\\test\" && " + cmd2);
        // builder1 = builder1.directory();
        final Process p1 = builder2.start();
        try {
            p1.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
//////Process to remove the code base///////////
        final String command3 = "RD /S /Q  C:\\test\\" + fileName;
        final ProcessBuilder builder3 = new ProcessBuilder("cmd.exe", "/c", "cd \"C:\\test\" && " + command3);
        final Process p3 = builder3.start();
        try {
            p3.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
/////Process to rename the filename with time stamp///////
        final long seconds = System.currentTimeMillis();
        final String rname = seconds + "-" + fileName + "-jscpd-report.html";

        final String command4 = "ren " + "jscpd-report.html " + rname;
        final ProcessBuilder builder5 = new ProcessBuilder("cmd.exe", "/c", "cd \"C:\\test\" && " + command4);
        final Process p4 = builder5.start();
        try {
            p4.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
/////Process to open the report//////////
        final String cmd3 = "start " + rname;
        final ProcessBuilder builder4 = new ProcessBuilder("cmd.exe", "/c", "cd \"C:\\test\" && " + cmd3);
        final Process p2 = builder4.start();
        try {
            p2.waitFor();
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
/////Process to log the report path//////////
        final String excelFilePath = "C:\\test\\Data_log.xlsx";
        final FileInputStream inputStream = new FileInputStream(new File(excelFilePath));
        final Workbook workbook = WorkbookFactory.create(inputStream);

        final Sheet sheet = workbook.getSheetAt(0);

        final int rowCount = sheet.getLastRowNum();
        final Row row = sheet.getRow(rowCount);
        final int columnCount = 1;

        final Cell cell = row.createCell(columnCount);
        cell.setCellValue("C:\\test\\" + rname);

        inputStream.close();

        final FileOutputStream outputStream = new FileOutputStream("C:\\test\\Data_log.xlsx");
        workbook.write(outputStream);
        workbook.close();
        outputStream.close();

        System.out.println("Got your Report");

        return "Final";

    }

}
