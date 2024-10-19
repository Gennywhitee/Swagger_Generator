@Entity
@Table(name="obj")
public class Obj implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long mId;

    @Column(name="user_id")
    private long mUserId;

    @Column(name="content")
    private String mContent;

    @Column(name="caso")
    private String mCaso;

    @OneToOne
    @JoinColumn(name="user")
    private User utente;

}