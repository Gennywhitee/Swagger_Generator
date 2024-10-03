@Entity
@Table(name="poll")
public class Poll implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long mId;

    @Column(name="user_id")
    private long mUserId;

    @Column(name="question")
    private String m_domanda;

    @Column(name="date_created")
    private Date data_creazione;
    
    @OneToOne
    @JoinColumn(name="Obj_id")
    private Obj id_oggetto;

    @OneToOne
    @JoinColumn(name="comment")
    private Comment commento;


}