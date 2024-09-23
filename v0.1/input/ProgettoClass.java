import jakarta.persistence.*;
import java.io.Serializable;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "progetto")
public class ProgettoClass implements Serializable {

    // Identificativo univoco del progetto
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private long id;

    // Nome del progetto
    @Column(name = "nome", nullable = false)
    private String nome;

    // Descrizione del progetto
    @Column(name = "descrizione")
    private String descrizione;

    // Data di inizio del progetto
    @Column(name = "data_inizio")
    @Temporal(TemporalType.DATE)
    private Date dataInizio;

    // Data di fine del progetto
    @Column(name = "data_fine")
    @Temporal(TemporalType.DATE)
    private Date dataFine;

    // Entità associata al progetto (campo complesso)
    @ManyToOne
    @JoinColumn(name = "entity_id", nullable = false)
    private EntityClass entityAssociata;

    // Costruttore vuoto obbligatorio per JPA
    public ProgettoClass() {
    }

    // Costruttore con parametri
    public ProgettoClass(String nome, String descrizione, Date dataInizio, Date dataFine, EntityClass entityAssociata) {
        this.nome = nome;
        this.descrizione = descrizione;
        this.dataInizio = dataInizio;
        this.dataFine = dataFine;
        this.entityAssociata = entityAssociata;
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

    public Date getDataInizio() {
        return dataInizio;
    }

    public void setDataInizio(Date dataInizio) {
        this.dataInizio = dataInizio;
    }

    public Date getDataFine() {
        return dataFine;
    }

    public void setDataFine(Date dataFine) {
        this.dataFine = dataFine;
    }

    public EntityClass getEntityAssociata() {
        return entityAssociata;
    }

    public void setEntityAssociata(EntityClass entityAssociata) {
        this.entityAssociata = entityAssociata;
    }

}
