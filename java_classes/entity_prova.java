import jakarta.persistence.*;
import java.io.Serializable;
import java.util.Date;

@Entity
@Table(name = "entity")
public class EntityClass implements Serializable {

    // Identificativo univoco dell'entità
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private long id;

    // Nome dell'entità
    @Column(name = "nome", nullable = false)
    private String nome;

    // Descrizione dell'entità
    @Column(name = "descrizione")
    private String descrizione;

    // Settore dell'entità
    @Column(name = "settore")
    private String settore;

    // Visione dell'entità
    @Column(name = "visione")
    private String visione;

    // Anno di fondazione
    @Column(name = "anno_fondazione")
    private int annoFondazione;

    // Sede dell'entità
    @Column(name = "sede")
    private String sede;

    // Data di creazione dell'entità nel sistema
    @Column(name = "data_creazione")
    @Temporal(TemporalType.TIMESTAMP)
    private Date dataCreazione;

    // Costruttore vuoto obbligatorio per JPA
    public EntityClass() {
    }

    // Costruttore con parametri
    public EntityClass(String nome, String descrizione, String settore, String visione, int annoFondazione, String sede, Date dataCreazione) {
        this.nome = nome;
        this.descrizione = descrizione;
        this.settore = settore;
        this.visione = visione;
        this.annoFondazione = annoFondazione;
        this.sede = sede;
        this.dataCreazione = dataCreazione;
    }

    // Getter e setter per i campi

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getDescrizione() {
        return descrizione;
    }

    public void setDescrizione(String descrizione) {
        this.descrizione = descrizione;
    }

    public String getSettore() {
        return settore;
    }

    public void setSettore(String settore) {
        this.settore = settore;
    }

    public String getVisione() {
        return visione;
    }

    public void setVisione(String visione) {
        this.visione = visione;
    }

    public int getAnnoFondazione() {
        return annoFondazione;
    }

    public void setAnnoFondazione(int annoFondazione) {
        this.annoFondazione = annoFondazione;
    }

    public String getSede() {
        return sede;
    }

    public void setSede(String sede) {
        this.sede = sede;
    }

    public Date getDataCreazione() {
        return dataCreazione;
    }

    public void setDataCreazione(Date dataCreazione) {
        this.dataCreazione = dataCreazione;
    }
}
