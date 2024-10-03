@Entity
@Table(name="comment")
public class Comment implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long mId;

    @Column(name="user_id")
    private long mUserId;

    @Column(name="content")
    private String m_commento;

    @Column(name="date_created")
    private Date m_d_creata;

}