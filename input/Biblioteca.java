package org.example;

public class Biblioteca implements Measurable, Comparable<Biblioteca>{
    private String title;
    private String author;
    private int year;

    public Biblioteca(){
        title= "";
        author="";
        year=0;
    }
    public Biblioteca(String title, String author, int year) {
        this.title=title;
        this.author=author;
        this.year=year;
    }
    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        if(controlloTitle(title)) {
            this.title=title;
        }else {
            this.title="";
        }
    }
    public void setAuthor(String author) {
        if(controlloAuthor(author)) {
            this.author=author;
        }else {
            this.author="";
        }
    }
    public String getAuthor() {
        return author;
    }
    public int getYear() {
        return year;
    }
    public void setYear(int year) {
        if(controlloYear(year)) {
            this.year=year;
        }else {
            this.year=0;
        }
    }
    public boolean controlloAuthor(String author) {
        if (author!=null) {
            return true;
        }else {
            return false;
        }
    }
    public boolean controlloTitle(String title) {
        if (title!=null) {
            return true;
        }else {
            return false;
        }
    }
    public boolean controlloYear(int year) {
        if(year<=2023) {
            return true;
        }
        return false;
    }

    @Override
    public int getMeasure() {
        return 2023 - this.year;
    }

    @Override
    public int compareTo(Biblioteca b) {
        return Integer.compare(b.getMeasure(), this.getMeasure());
    }
}