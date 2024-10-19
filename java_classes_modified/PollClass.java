@Entity
@Table(name="poll")
public class Poll implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long pollId;

    @Column(name="user_id")
    private long userId;

    @Column(name="question")
    private String question;

    @Column(name="date_created")
    private Date dateCreated;
    
    @OneToOne
    @JoinColumn(name="Obj_id")
    private Obj obj;

    @OneToOne
    @JoinColumn(name="comment")
    private Comment comment;

}

